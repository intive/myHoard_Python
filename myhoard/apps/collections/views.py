from flask.ext.restful import Resource, marshal_with, marshal, fields
from flask import request
from datetime import datetime
from mongoengine import ValidationError
import time

from models import Collection
from parsers import CollectionForm

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

# errors marshal fields
error_fields = {
    'error_code': fields.Integer,
    'errors': fields.Raw
}

# TODO authorization
class Collections(Resource):
    def get(self, id):
        try:
            collection = Collection.objects.get(id=id)
        except ValidationError, ve:
            response = {'error_code': 404, 'errors': {'collection': str(ve)}}
            return marshal(response, error_fields), 404
        return marshal(collection, collection_fields)

    # TODO validation
    def put(self, id):
        try:
            collection = Collection.objects.get(id=id)
        except ValidationError, ve:
            response = {'error_code': 404, 'errors': {'collection': str(ve)}}
            return marshal(response, error_fields), 404
        # create validation form from json request
        form = CollectionForm.from_json(request.json)
        if form.validate():
            form.populate_obj(collection)
            collection.modified_date = getCurrentTime()
            collection.save()
            return marshal(collection, collection_fields)
        else:
            response = {"error_code": 400, "errors": form.errors}
            return marshal(response, error_fields), 400


    def delete(self, id):
        try:
            collection = Collection.objects.get(id=id)
        except ValidationError, ve:
            response = {'error_code': 404, 'errors': {'collection': str(ve)}}
            return marshal(response, error_fields), 404
        collection.delete()
        return '', 204


# TODO authorization
class CollectionsList(Resource):
    def post(self):
        # create validation form from json request
        form = CollectionForm.from_json(request.json)
        if form.validate():
            collection = Collection(
                name=form.name.data,
                description=form.description.data,
                tags=form.tags.data,
                # TODO get/set items_number
                items_number=0,
                created_date=getCurrentTime(),
                modified_date=getCurrentTime(),
                # TODO get owner
                owner="TODO owner"
            )
            collection.save()
            return marshal(collection, collection_fields)
        else:
            response = {"error_code": 400, "errors": form.errors}
            return marshal(response, error_fields), 400

    @marshal_with(collection_fields)
    def get(self):
        return list(Collection.objects)


def getCurrentTime():
    time_zone = str.format('{0:+06.2f}', -float(time.timezone) / 3600)
    datetime_now = "%s%s" % (datetime.now().isoformat(), time_zone)
    return datetime_now


def demo():
    return "demo"