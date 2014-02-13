from flask.ext.restful import Resource, marshal_with, fields
from flask import request
from datetime import datetime
from models import Collection

collection_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'tags': fields.String,
    'items_number': fields.Integer,
    'created_date': fields.String,
    'modified_date': fields.String,
    'owner': fields.String
}

# TODO authorization
# TODO validation
class Collections(Resource):
    def __init__(self):
        super(Collections, self).__init__()

    @marshal_with(collection_fields)
    def get(self, id):
        # TODO 404 if collection not exist
        return Collection.objects.get(id=id)

    def put(self):
        pass

    def delete(self, id):
        collection = Collection.objects.get(id=id)
        collection.delete()
        # TODO 404 if collection not exist
        return '', 204

# TODO authorization
# TODO validation
class CollectionsList(Resource):
    def __init__(self):
        super(CollectionsList, self).__init__()

    @marshal_with(collection_fields)
    def post(self):
        collection = Collection(
            name=request.json['name'],
            description=request.json['description'],
            tags=request.json['tags'],
            # TODO get/set items_number
            items_number=0,
            created_date=str(datetime.now().isoformat()),
            modified_date=str(datetime.now().isoformat()),
            # TODO get owner
            owner="TODO owner"
        )
        collection.save()
        return collection, 201

    @marshal_with(collection_fields)
    def get(self):
        return list(Collection.objects)


def demo():
    return "demo"