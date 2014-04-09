from flask import request
from flask.ext.restful import Resource, marshal_with, fields

from myhoard.apps.common.utils import get_request_json
from myhoard.apps.auth.decorators import login_required
from myhoard.apps.collections.items.views import item_fields
from myhoard.apps.collections.items.models import Item
from myhoard.apps.collections.comments.views import comment_fields
from myhoard.apps.collections.comments.models import Comment
from myhoard.apps.auth.models import User

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
    'public': fields.Boolean,
}


class CollectionDetails(Resource):
    method_decorators = [marshal_with(collection_fields), login_required]

    @staticmethod
    def get(collection_id):
        return Collection.objects.get_or_404(id=collection_id)

    @staticmethod
    def put(collection_id):
        return Collection.update(collection_id, **get_request_json())

    @staticmethod
    def delete(collection_id):
        Collection.delete(collection_id)

        return '', 204


class CollectionList(Resource):
    method_decorators = [marshal_with(collection_fields), login_required]

    @staticmethod
    def post():
        return Collection.create(**get_request_json())

    @staticmethod
    def get():
        return list(Collection.get_ordered(request.values))


class CollectionItemList(Resource):
    method_decorators = [marshal_with(item_fields), login_required]

    @staticmethod
    def get(collection_id):
        Collection.objects.get_or_404(id=collection_id)
        return list(Item.get_ordered(request.values, collection_id))


class CollectionCommentList(Resource):
    method_decorators = [marshal_with(comment_fields), login_required]

    @staticmethod
    def get(collection_id):
        Collection.objects.get_or_404(id=collection_id)
        return list(Comment.objects(collection=collection_id))


class UserPublicCollectionList(Resource):
    method_decorators = [marshal_with(collection_fields), login_required]

    @staticmethod
    def get(user_id):
        User.objects.get_or_404(id=user_id)
        return list(Collection.objects(owner=user_id, public=True))