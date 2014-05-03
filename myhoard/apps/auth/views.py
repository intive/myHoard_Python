from flask.ext.restful import Resource, fields, marshal_with
from myhoard.apps.auth.decorators import login_required
import logging

from myhoard.apps.common.utils import get_request_json
from models import User

logger = logging.getLogger(__name__)

user_fields = {
    'username': fields.String,
    'email': fields.String,
}


class UserDetails(Resource):
    method_decorators = [marshal_with(user_fields), login_required]

    @staticmethod
    def get(user_id):
        return User.objects.get_or_404(id=user_id)

    @staticmethod
    def put(user_id):
        return User.put(user_id, **get_request_json())

    @staticmethod
    def patch(user_id):
        return User.patch(user_id, **get_request_json())

    @staticmethod
    def delete(user_id):
        User.delete(user_id)
        return '', 204


class UserList(Resource):
    method_decorators = [marshal_with(user_fields)]

    def post(self):
        return User.create(**get_request_json()), 201

    @staticmethod
    def get():
        return list(User.objects)