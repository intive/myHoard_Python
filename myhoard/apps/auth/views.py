from werkzeug.security import generate_password_hash
from flask.ext.restful import Resource, fields, marshal_with

from myhoard.apps.common.decorators import custom_errors
from myhoard.apps.common.utils import get_request_json

from models import User

user_fields = {
    'username': fields.String,
    'email': fields.String,
}


class Users(Resource):
    method_decorators = [marshal_with(user_fields), custom_errors]

    def post(self):
        user = User(**get_request_json())
        if user.password:
            user.password = generate_password_hash(user.password)
        user.save()
        return user, 201