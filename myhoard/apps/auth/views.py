from flask.ext.restful import Resource, fields, marshal_with

from models import User
from myhoard.apps.common.utils import custom_errors, get_request_json
from myhoard.apps.common.security import generate_password_hash

user_fields = {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
}


class Users(Resource):
    method_decorators = [marshal_with(user_fields), custom_errors]

    def post(self):
        user = User(**get_request_json())
        user['password'] = generate_password_hash(user['password'])
        user.save()
        return user, 201