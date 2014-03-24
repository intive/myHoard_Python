from bson.errors import InvalidId
from bson.objectid import ObjectId

from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound

from errors import handle_custom_errors

class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(value)
        except (InvalidId, TypeError):
            handle_custom_errors(NotFound())

    def to_url(self, value):
        return str(value)