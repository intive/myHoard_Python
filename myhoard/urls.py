from flask.ext.restful import Api
from flask import current_app
from myhoard.apps.collections.views import Collections, demo
from myhoard.apps.auth.views import Users


# register the urls
current_app.add_url_rule('/', view_func=demo)

# restful api
api = Api(current_app)
api.add_resource(Collections, '/collections/')
api.add_resource(Users, '/users/')