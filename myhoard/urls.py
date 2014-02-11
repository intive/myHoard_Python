from flask.ext.restful import Api
from flask import current_app

from myhoard.apps.collections.views import Collections, demo
from myhoard.apps.users.views import Users


# register the urls
current_app.add_url_rule('/', view_func=demo)

# restful api
current_app.api.add_resource(Collections, '/collections/')
current_app.api.add_resource(Users, '/users/')