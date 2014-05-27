from importlib import import_module
import logging

from flask import request, g
from mongoengine import ValidationError, Q
from bson.errors import InvalidId
from bson.objectid import ObjectId

logger = logging.getLogger(__name__)


def get_request_json():
    '''Returns parsed JSON data from flask request, throws ValidationError on fail'''
    json = request.get_json(silent=True)
    if not json:
        raise ValidationError('No incoming JSON data')

    logger.debug('get_request_json dump:\njson: {}'.format(json))

    return json


def load_class(path):
    '''Dynamically loads and returns class from given path'''
    mod, cls = path.rsplit('.', 1)
    mod = import_module(mod)

    logger.debug('load_class dump:\nmod: {}\ncls: {}'.format(mod, cls))

    return getattr(mod, cls)


def string_to_object_id(string_id):
    '''Convert string id to ObjectId'''
    try:
        return ObjectId(string_id)
    except InvalidId:
        logger.debug('string_to_object_id dump:\nstring_id: {}\nInvalidId!'.format(string_id))

        return None


# TODO RT remove
def make_order_by_for_query(params):
    '''Returns mongolike sort_by prefixed with directions from given flask params'''
    directions = {'asc': '+', 'desc': '-'}

    sort_by = params.getlist('sort_by')
    sort_direction = params.get('sort_direction')

    direction = directions.get(sort_direction, '+')
    order_by = [direction + s for s in sort_by]

    logger.debug('make_order_by_for_query dump:\norder_by: {}'.format(order_by))

    return order_by


# TODO RT remove
def make_collection_search_query(params):
    '''Returns collection search query'''
    raw_queries = {
        'name': {'$regex': params.get('name'), '$options': 'i'},
        'description': {'$regex': params.get('description'), '$options': 'i'},
        '$or': [
            {'owner': g.user}, {'public': True}
        ]
    }

    owner = params.get('owner')
    if owner:
        raw_queries['owner'] = string_to_object_id(owner)

    logger.debug('make_collection_search_query dump:\nowner: {}\nraw_queries: {}'.format(owner, raw_queries))

    return Q(__raw__=raw_queries)


def make_item_search_query(params, collection_id):
    '''Returns item search query'''
    raw_queries = {
        'name': {'$regex': params.get('name'), '$options': 'i'},
        'description': {'$regex': params.get('description'), '$options': 'i'},
        'collection': collection_id
    }

    # Geolocation search
    if 'geo' in params:
        geo = params.get('geo')
        max_range = float(params.get('max_range', 10000))
        geo = geo.split(',')
        location = {'lat': float(geo[0]), 'lng': float(geo[1])}

        # http://docs.mongodb.org/manual/reference/operator/query/near/
        raw_queries['location'] = {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [location.get('lng'), location.get('lat')]
                },
                '$maxDistance': max_range
            }
        }

        logger.debug('make_item_search_query dump:\ngeo: {}\nraw_queries: {}'.format(geo, raw_queries))
    else:
        logger.debug('make_item_search_query dump:\nraw_queries: {}'.format(raw_queries))

    return Q(__raw__=raw_queries)


# TODO RT refactor
def make_pipeline(params):
    '''
        Returns aggregation pipeline
        http://docs.mongodb.org/manual/reference/operator/aggregation-pipeline/
    '''
    # sort directions
    directions = {'asc': 1, 'desc': -1}
    # params
    sort_by = params.getlist('sort_by')
    sort_direction = params.get('sort_direction')

    direction = directions.get(sort_direction, 1)
    if not sort_by:
        sort_by = ['name']

    pipeline = [
        {
            '$project': {
                'id': '$_id',
                'name': '$name',
                'name_lower': {'$toLower': '$name'},
                'description': '$description',
                'description_lower': {'$toLower': '$description'},
                'tags': '$tags',
                'items_count': '$items_count',
                'created_date': '$created_date',
                'modified_date': '$modified_date',
                'owner': '$owner',
                'public': '$public',
            }
        },
        {
            # example 'sort': {name_lower: 1} sorts collections by name (case insensitive)
            '$sort': {s + '_lower': direction for s in sort_by},
        },
        {
            '$match': {
                'name': {'$regex': params.get('name'), '$options': 'i'},
                'description': {'$regex': params.get('description'), '$options': 'i'},
                '$or': [{'owner': g.user}, {'public': True}],
            }
        }
    ]

    owner = params.get('owner')
    if owner:
        pipeline[2]['$match']['owner'] = string_to_object_id(owner)

    logger.debug('make_pipeline dump:\npipeline: {}'.format(pipeline))

    return pipeline

# TODO RT pipeline for items
# TODO RT geo search http://docs.mongodb.org/manual/reference/operator/aggregation/geoNear/
