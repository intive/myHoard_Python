from datetime import datetime

from flask import g, url_for
from flask.ext.restful import Resource, marshal_with, fields

from myhoard.apps.common.decorators import custom_errors
from myhoard.apps.common.utils import get_request_json
from myhoard.apps.common.errors import FileError
from myhoard.apps.auth.decorators import login_required
from myhoard.apps.collections.models import Collection
from myhoard.apps.collections.items.models import Item
from myhoard.apps.media.models import Medium


# custom geo location field
class GeoLocationField(fields.Raw):
    def format(self, point):
        return {'lat': point[0], 'lng': point[1]}


# custom media field
class MediaField(fields.Raw):
    def format(self, media_id):
        return {
            'id': str(media_id),
            'url': url_for('mediadetails', id=media_id, _external=True)
        }

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


class ItemDetails(Resource):
    method_decorators = [marshal_with(item_fields), login_required,
                         custom_errors]

    def get(self, id):
        item = Item.objects.get(id=id)

        return item

    def put(self, id):
        item = Item.objects.get(id=id)
        update_item = Item(**get_request_json())
        item.name = update_item.name
        item.description = update_item.description
        item.quantity = update_item.quantity
        item.location = (
            update_item.location['lat'],
            update_item.location['lng'],
        )
        item.collection = update_item.collection

        for medium_id in item.media:
            medium = Medium.objects.get(id=medium_id)
            if medium_id not in update_item.media:
                medium.delete()
            else:
                if not medium.collection or medium.collection == item.collection:
                    medium.collection = item.collection
                    medium.save()
                else:
                    raise FileError(
                        'ERROR_CODE_MEDIA_ALREADY_HAVE_PARENT',
                        errors={'media': {medium_id: 'Media already have parent'}}
                    )

        item.media = update_item.media
        item.modified_date = datetime.now()
        item.save()

        return item

    def delete(self, id):
        item = Item.objects.get(id=id)

        collection = Collection.objects.get(id=item.collection)
        collection.items_count -= 1
        collection.save()

        for medium_id in item.media:
            medium = Medium.objects.get(id=medium_id)
            medium.delete()

        item.delete()

        return '', 204


class ItemList(Resource):
    method_decorators = [marshal_with(item_fields), login_required,
                         custom_errors]

    def post(self):
        item = Item(**get_request_json())
        # TODO Move to model
        item.owner = g.user
        item.created_date = datetime.now()
        item.modified_date = datetime.now()
        item.location = (item.location['lat'], item.location['lng'])

        collection = Collection.objects.get(id=item.collection)
        collection.items_count += 1
        collection.save()

        # TODO Move to model
        for medium_id in item.media:
            medium = Medium.objects.get(id=medium_id)
            if not medium.collection:
                medium.collection = item.collection
            else:
                raise FileError(
                    'ERROR_CODE_MEDIA_ALREADY_HAVE_PARENT',
                    errors={'media': {medium_id: 'Media already have parent'}}
                )
            medium.save()

        item.save()

        return item, 201

    def get(self):
        return list(Item.objects)
