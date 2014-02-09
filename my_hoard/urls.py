from flask import Blueprint
urls = Blueprint('urls', __name__)

from flask.ext.restful import Api
from my_hoard.apps.collections.views import Collections, demo
from my_hoard.apps.auth.views import Users

# register the urls
urls.add_url_rule('/', view_func=demo)

# restful api
api = Api(urls)
api.add_resource(Collections, '/collections/')
api.add_resource(Users, '/users/')