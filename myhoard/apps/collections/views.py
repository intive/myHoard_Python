from datetime import datetime

from flask import g, request
from flask.ext.restful import Resource, marshal_with, fields

from myhoard.apps.common.decorators import custom_errors
from myhoard.apps.common.utils import get_request_json
from myhoard.apps.auth.decorators import login_required

from models import Collection

collection_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'tags': fields.List(fields.String),
    'items_number': fields.Integer,
    'created_date': fields.String,
    'modified_date': fields.String,
    'owner': fields.String,
}


class Collections(Resource):
    method_decorators = [marshal_with(collection_fields), login_required, custom_errors]

    def get(self, id):
        collection = Collection.objects.get(id=id)

        return collection

    def put(self, id):
        collection = Collection.objects.get(id=id)
        update_collection = Collection(**get_request_json())
        collection.name = update_collection.name
        collection.description = update_collection.description
        collection.tags = update_collection.tags
        collection.modified_date = datetime.now()
        collection.save()

        return collection

    def delete(self, id):
        collection = Collection.objects.get(id=id)
        collection.delete()

        return '', 204


class CollectionsList(Resource):
    method_decorators = [marshal_with(collection_fields), login_required, custom_errors]

    def post(self):
        collection = Collection(**get_request_json())
        collection.owner = g.user
        collection.created_date = datetime.now()
        collection.modified_date = datetime.now()
        collection.save()

        return collection, 201

    def get(self):
        # TODO sort
        sort_by = request.values.getlist('sort_by')
        sort_direction = request.values.get('sort_direction')
        #geo = request.values.get('geo')

        # order direction + == asc, - == desc
        try:
            dir = {'asc': '+', 'desc': '-'}[sort_direction]
        except KeyError:
            dir = '+'

        # setting direction sorting elements
        order_by = [dir + s for s in sort_by]

        # sorting
        sorted_collections = Collection.objects.order_by(*order_by)

        return list(sorted_collections)