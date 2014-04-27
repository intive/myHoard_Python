from importlib import import_module
import logging

from flask import request, g
from mongoengine import ValidationError, Q
from bson.errors import InvalidId
from bson.objectid import ObjectId

logger = logging.getLogger(__name__)


def get_request_json():
    """returns parsed JSON data from flask request, throws ValidationError on fail"""
    json = request.get_json(silent=True)
    if not json:
        raise ValidationError('No incoming JSON data')

    return json


def load_class(path):
    """Dynamically loads and returns class from given path"""
    mod, cls = path.rsplit('.', 1)
    mod = import_module(mod)
    return getattr(mod, cls)


def string_to_object_id(string_id):
    """Convert string id to ObjectId"""
    try:
        return ObjectId(string_id)
    except InvalidId:
        logger.debug('string id: {0} is invalid'.format(string_id))
        return None


def make_order_by_for_query(params):
    """Returns mongolike sort_by prefixed with directions from given flask params"""
    directions = {'asc': '+', 'desc': '-'}

    sort_by = params.getlist('sort_by')
    sort_direction = params.get('sort_direction')

    direction = directions.get(sort_direction, '+')
    order_by = [direction + s for s in sort_by]

    return order_by


def make_collection_search_query(params):
    """Returns collection search query"""
    raw_queries = {
        'name': {'$regex': params.get('name')},
        'description': {'$regex': params.get('description')},
        '$or': [
            {'owner': g.user}, {'public': True}
        ]
    }

    owner = params.get('owner')
    if owner:
        raw_queries['owner'] = string_to_object_id(owner)

    logger.debug('make_collection_search_query\n owner: {0}\n raw_queries: {1}'.format(owner, raw_queries))

    return Q(__raw__=raw_queries)


def make_item_search_query(params, collection_id):
    """Returns item search query"""
    raw_queries = {
        'name': {'$regex': params.get('name')},
        'description': {'$regex': params.get('description')},
        'collection': collection_id
    }

    # geolocation search
    geo = params.get('geo')
    if geo:
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

    logger.debug('make_item_search_query\n geo: {0}\n raw_queries: {1}'.format(geo, raw_queries))

    return Q(__raw__=raw_queries)