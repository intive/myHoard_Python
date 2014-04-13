from flask import current_app

from myhoard.api import landingpage
from myhoard.apps.auth.oauth.views import oauth
from myhoard.apps.auth.views import UserList, UserDetails
from myhoard.apps.collections.views import CollectionDetails, CollectionList, \
    CollectionItemList, CollectionCommentList, UserPublicCollectionList
from myhoard.apps.collections.items.views import ItemDetails, ItemList
from myhoard.apps.media.views import MediaDetails, MediaList
from myhoard.apps.collections.comments.views import CommentDetails, CommentList

# Top scope urls
current_app.add_url_rule('/', view_func=landingpage, methods=['GET'])
current_app.add_url_rule('/oauth/token/', view_func=oauth, methods=['POST'])

# Blueprint urls
current_app.api.add_resource(UserList, '/users/')
current_app.api.add_resource(UserDetails, '/users/<ObjectId:user_id>/')
current_app.api.add_resource(UserPublicCollectionList, '/users/<ObjectId:user_id>/collections/')

current_app.api.add_resource(CollectionDetails, '/collections/<ObjectId:collection_id>/')
current_app.api.add_resource(CollectionList, '/collections/')
current_app.api.add_resource(CollectionItemList, '/collections/<ObjectId:collection_id>/items/')
current_app.api.add_resource(CollectionCommentList, '/collections/<ObjectId:collection_id>/comments/')

current_app.api.add_resource(ItemDetails, '/items/<ObjectId:item_id>/')
current_app.api.add_resource(ItemList, '/items/')

current_app.api.add_resource(MediaDetails, '/media/<ObjectId:media_id>/', '/media/<ObjectId:media_id>/thumbnail')
current_app.api.add_resource(MediaList, '/media/')

current_app.api.add_resource(CommentDetails, '/comments/<ObjectId:comment_id>/')
current_app.api.add_resource(CommentList, '/comments/')