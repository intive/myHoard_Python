from flask.ext.restful import reqparse, types

user_post_reqparse = reqparse.RequestParser()
user_post_reqparse.add_argument('username', type=str, required=True)
user_post_reqparse.add_argument('email', type=str, required=True)
user_post_reqparse.add_argument('password', type=str, required=True)