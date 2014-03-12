from mongoengine import Document, StringField, ListField, IntField, \
    ObjectIdField, DateTimeField


class Collection(Document):
    name = StringField(min_length=3, max_length=20, required=True)
    description = StringField(min_length=3, max_length=50, required=True)
    tags = ListField(StringField(min_length=3, max_length=10))
    items_count = IntField(min_value=0)
    created_date = DateTimeField()
    modified_date = DateTimeField()
    owner = ObjectIdField()