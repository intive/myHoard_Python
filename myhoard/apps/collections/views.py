from flask.ext.restful import Resource, marshal_with, marshal, fields
from datetime import datetime
from myhoard.apps.common.decorators import custom_errors
from myhoard.apps.common.utils import get_request_json
from models import Collection
import time

# collection marshal fields
collection_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'tags': fields.List(fields.String),
    'items_number': fields.Integer,
    'created_date': fields.String,
    'modified_date': fields.String,
    'owner': fields.String
}

# TODO authorization
class Collections(Resource):
    method_decorators = [marshal_with(collection_fields), custom_errors]

    def get(self, id):
        collection = Collection.objects.get(id=id)
        return collection

    def put(self, id):
        collection = Collection.objects.get(id=id)
        update_collection = Collection(**get_request_json())
        collection.name = update_collection.name
        collection.description = update_collection.description
        collection.tags = update_collection.tags
        collection.modified_date = get_datetime()
        collection.save()
        return collection

    def delete(self, id):
        collection = Collection.objects.get(id=id)
        collection.delete()
        return '', 204


# TODO authorization
class CollectionsList(Resource):
    method_decorators = [marshal_with(collection_fields), custom_errors]

    def post(self):
        collection = Collection(**get_request_json())
        collection.created_date = get_datetime()
        collection.modified_date = get_datetime()
        # TODO get owner
        collection.owner = "TODO owner"
        collection.save()
        return collection, 201


    def get(self):
        return list(Collection.objects)

# return current date and time zone, format Y-m-dTH:M:S+HH:MM
def get_datetime():
    return str.format('{0}{1:+06.2f}', datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), -float(time.timezone) / 3600)