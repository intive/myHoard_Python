from flask import current_app

from myhoard import api
from myhoard.apps.collections.views import Collections, CollectionsList
from myhoard.apps.auth.views import Users
from myhoard.apps.auth.oauth.views import oauth
from myhoard.apps.collections.items.views import Items, ItemsList

# register the urls
current_app.add_url_rule('/', view_func=api.landingpage, methods=['GET'])
current_app.add_url_rule('/oauth/token/', view_func=oauth, methods=['POST'])

# restful api
current_app.api.add_resource(Collections, '/collections/<string:id>/')
current_app.api.add_resource(CollectionsList, '/collections/')
current_app.api.add_resource(Users, '/users/')
current_app.api.add_resource(Items, '/items/<string:id>/')
current_app.api.add_resource(ItemsList, '/items/')
