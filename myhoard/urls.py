from flask import current_app

from myhoard.apps.collections.views import Collections
from myhoard.apps.auth.views import Users
from myhoard.apps.auth.oauth.views import oauth


# register the urls
current_app.add_url_rule('/oauth/token/', view_func=oauth, methods=['POST'])

# restful api
current_app.api.add_resource(Collections, '/collections/')
current_app.api.add_resource(Users, '/users/')