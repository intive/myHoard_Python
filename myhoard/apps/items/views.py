from flask.ext.restful import Resource, marshal_with, fields
from myhoard.apps.common.decorators import custom_errors, login_required

# TODO geolocation marshal fields
location_fields = {
    'lat': fields.Float(attribute='lat'),
    'lng': fields.Float(attribute='lng')
}

# TODO media marshal fields
media_fields = {
    'id': fields.String(attribute='id'),
    'url': fields.String(attribute='url')
}

# item marshal fields
item_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'location': fields.Nested(location_fields),
    'quantity': fields.Integer,
    'media': fields.List(fields.Nested(media_fields)), # TODO media objects list
    'created_date': fields.String,
    'modified_date': fields.String,
    'collection': fields.String,
    'owner': fields.String
}

# TODO
class Items(Resource):
    method_decorators = [marshal_with(item_fields), login_required,
                         custom_errors]

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

# TODO
class ItemsList(Resource):
    method_decorators = [marshal_with(item_fields), login_required,
                         custom_errors]

    def post(self):
        # TODO set collection fk to all media objects
        pass

    def get(self):
        return {}
