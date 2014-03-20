from datetime import datetime

from flask import g, request
from flask.ext.restful import Resource, marshal_with, fields, marshal

from myhoard.apps.common.decorators import custom_errors
from myhoard.apps.common.utils import get_request_json
from myhoard.apps.auth.decorators import login_required
from myhoard.apps.collections.items.views import item_fields
from myhoard.apps.collections.items.models import Item

from models import Collection

collection_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'tags': fields.List(fields.String),
    'items_count': fields.Integer,
    'created_date': fields.String,
    'modified_date': fields.String,
    'owner': fields.String,
}


class CollectionDetails(Resource):
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


class CollectionList(Resource):
    method_decorators = [login_required, custom_errors]

    def post(self):
        collection = Collection(**get_request_json())
        collection.items_count = 0
        collection.owner = g.user
        collection.created_date = datetime.now()
        collection.modified_date = datetime.now()
        collection.save()

        return marshal(collection, collection_fields), 201

    def get(self):
        sort_by = request.values.getlist('sort_by')
        sort_direction = request.values.get('sort_direction')

        # order direction + == asc, - == desc
        try:
            dir = {'asc': '+', 'desc': '-'}[sort_direction]
        except KeyError:
            dir = '+'

        # setting direction sorting elements
        order_by = [dir + s for s in sort_by]

        # sorting
        sorted_collections = Collection.objects(owner=g.user).order_by(*order_by)

        return {"total_count": len(sorted_collections),
                "collections": marshal(list(sorted_collections), collection_fields)}


class CollectionItemList(Resource):
    method_decorators = [marshal_with(item_fields), login_required, custom_errors]

    def get(self, id):
        # TODO check if collection exists first
        # TODO use all() method instead
        return list(Item.objects(owner=g.user, collection=id))

