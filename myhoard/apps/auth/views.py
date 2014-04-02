from flask.ext.restful import Resource, fields, marshal_with

from myhoard.apps.common.utils import get_request_json

from models import User

user_fields = {
    'username': fields.String,
    'email': fields.String,
}


# TODO shouldn't it be UserList
class UserDetails(Resource):
    method_decorators = [marshal_with(user_fields)]

    def post(self):
        return User.create_user(**get_request_json()), 201