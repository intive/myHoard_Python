import logging
from flask.ext.restful import Resource, marshal_with, fields

from myhoard.apps.common.utils import get_request_json
from myhoard.apps.auth.decorators import login_required
from myhoard.apps.collections.comments.models import Comment

logger = logging.getLogger(__name__)

comment_fields = {
    'id': fields.String,
    'content': fields.String,
    'created_date': fields.String,
    'collection': fields.String,
    'owner': fields.String
}


class CommentDetails(Resource):
    method_decorators = [marshal_with(comment_fields), login_required]

    @staticmethod
    def get(comment_id):
        return Comment.objects.get_or_404(id=comment_id)

    @staticmethod
    def put(comment_id):
        return Comment.update(comment_id, **get_request_json())

    @staticmethod
    def delete(comment_id):
        Comment.delete_(comment_id)

        return '', 204


class CommentList(Resource):
    method_decorators = [marshal_with(comment_fields), login_required]

    @staticmethod
    def post():
        return Comment.create(**get_request_json()), 201