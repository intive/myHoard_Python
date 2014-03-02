from datetime import datetime

from mongoengine import Document, StringField, ListField, IntField, \
    ObjectIdField, DateTimeField


class Collection(Document):
    name = StringField(min_length=3, max_length=20, required=True)
    description = StringField(min_length=3, max_length=50, required=True)
    tags = ListField(StringField(min_length=3, max_length=10))
    items_number = IntField(min_value=0)
    created_date = DateTimeField(default=datetime.now())
    modified_date = DateTimeField(default=datetime.now())
    owner = ObjectIdField()