from flask import current_app

from myhoard.api import landingpage, logs
from myhoard.apps.auth.oauth.views import oauth
from myhoard.apps.auth.views import UserDetails
from myhoard.apps.collections.views import CollectionDetails, CollectionList, \
    CollectionItemList
from myhoard.apps.collections.items.views import ItemDetails, ItemList
from myhoard.apps.media.views import MediaDetails, MediaList

# Top scope urls
current_app.add_url_rule('/', view_func=landingpage, methods=['GET'])
current_app.add_url_rule('/logs', view_func=logs, methods=['GET'])
current_app.add_url_rule('/oauth/token/', view_func=oauth, methods=['POST'])

# Blueprint urls
current_app.api.add_resource(UserDetails, '/users/')

current_app.api.add_resource(CollectionDetails,
                             '/collections/<objectid:collection_id>/')
current_app.api.add_resource(CollectionList, '/collections/')
current_app.api.add_resource(CollectionItemList,
                             '/collections/<objectid:collection_id>/items/')

current_app.api.add_resource(ItemDetails, '/items/<objectid:item_id>/')
current_app.api.add_resource(ItemList, '/items/')

current_app.api.add_resource(MediaDetails, '/media/<objectid:media_id>/',
                             '/media/<objectid:media_id>/thumbnail')
current_app.api.add_resource(MediaList, '/media/')