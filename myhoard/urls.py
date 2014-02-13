from flask import current_app

from myhoard.apps.collections.views import Collections, CollectionsList, demo
from myhoard.apps.auth.views import Users


# register the urls
current_app.add_url_rule('/', view_func=demo)

# restful api
current_app.api.add_resource(Collections, '/collections/<string:id>/')
current_app.api.add_resource(CollectionsList, '/collections/')
current_app.api.add_resource(Users, '/users/')