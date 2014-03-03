from datetime import datetime

from flask import g, current_app
from flask.ext.restful import Resource, marshal_with, fields

from myhoard.apps.common.decorators import custom_errors
from myhoard.apps.common.utils import get_request_json
from myhoard.apps.auth.decorators import login_required
from models import Item


# custom geo location field
class GeoLocationField(fields.Raw):
    def format(self, point):
        return {'lat': point[0], 'lng': point[1]}


# custom media field
class MediaField(fields.Raw):
    def format(self, id):
        return {'id': str(id), 'url': '%s/media/%s/' % (current_app.config['URL_SERVER'], str(id))}

# item marshal fields
item_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'location': GeoLocationField(),
    'quantity': fields.Integer,
    'media': fields.List(MediaField()),
    'created_date': fields.String,
    'modified_date': fields.String,
    'collection': fields.String,
    'owner': fields.String
}


class Items(Resource):
    method_decorators = [marshal_with(item_fields), login_required, custom_errors]

    def get(self, id):
        item = Item.objects.get(id=id)

        return item

    def put(self, id):
        item = Item.objects.get(id=id)
        update_item = Item(**get_request_json())
        item.name = update_item.name
        item.description = update_item.description
        item.quantity = update_item.quantity
        item.location = (update_item.location['lat'], update_item.location['lng'])
        item.collection = update_item.collection
        item.media = update_item.media
        item.modified_date = datetime.now()
        item.save()

        return item

    def delete(self, id):
        item = Item.objects.get(id=id)
        item.delete()

        return '', 204


class ItemsList(Resource):
    method_decorators = [marshal_with(item_fields), login_required, custom_errors]

    def post(self):
        item = Item(**get_request_json())
        item.owner = g.user
        item.created_date = datetime.now()
        item.modified_date = datetime.now()
        item.location = (item.location['lat'], item.location['lng'])
        item.save()

        return item, 201

    def get(self):
        return list(Item.objects)
