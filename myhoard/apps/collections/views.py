from flask import g, request
from flask.ext.restful import Resource, marshal_with, fields

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
    method_decorators = [marshal_with(collection_fields), login_required]

    @staticmethod
    def get(collection_id):
        return Collection.objects.get_or_404(id=collection_id)

    @staticmethod
    def put(collection_id):
        return Collection.update_collection(collection_id, **get_request_json())

    @staticmethod
    def delete(collection_id):
        Collection.delete_collection(collection_id)

        return '', 204


class CollectionList(Resource):
    method_decorators = [marshal_with(collection_fields), login_required]

    @staticmethod
    def post():
        return Collection.create_collection(**get_request_json())

    @staticmethod
    def get():
        sort_by = request.values.getlist('sort_by')
        sort_direction = request.values.get('sort_direction')

        # order direction + == asc, - == desc
        try:
            dir_ = {'asc': '+', 'desc': '-'}[sort_direction]
        except KeyError:
            dir_ = '+'

        # setting direction sorting elements
        order_by = [dir_ + s for s in sort_by]

        # sorting
        sorted_collections = Collection.objects(owner=g.user).order_by(
            *order_by)

        return list(sorted_collections)


class CollectionItemList(Resource):
    method_decorators = [marshal_with(item_fields), login_required]

    @staticmethod
    def get(collection_id):
        Collection.objects.get_or_404(id=collection_id)
        return list(Item.objects(owner=g.user, collection=collection_id))