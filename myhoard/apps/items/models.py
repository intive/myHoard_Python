from mongoengine import Document, StringField, ListField, IntField, \
    ObjectIdField, DateTimeField, GeoPointField
from datetime import datetime


class Item(Document):
    name = StringField(min_length=2, max_length=50, required=True)
    description = StringField(max_length=250)
    location = GeoPointField()
    quantity = IntField(min_value=0)
    created_date = DateTimeField(default=datetime.now())
    modified_date = DateTimeField(default=datetime.now())
    # TODO this list should contain media objects
    media = ListField()
    collection = ObjectIdField()
    owner = ObjectIdField()