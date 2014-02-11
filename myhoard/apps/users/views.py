from flask import abort
from flask.ext.restful import Resource, fields, marshal
from mongoengine import OperationError

from models import User
from parsers import user_post_reqparse

user_fields = {
    'username': fields.String,
    'email': fields.String,
}

class Users(Resource):
    def post(self):
    	args = user_post_reqparse.parse_args()
        user = User(**args);

        try:
        	user.save()
        except OperationError as e:
        	return {'error_code': 100}, 400

        return marshal(user, user_fields), 201