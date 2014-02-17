from mongoengine import Document, StringField, ListField, IntField


class Collection(Document):
    name = StringField(min_length=3, max_length=20, required=True)
    description = StringField(min_length=3, max_length=50, required=True)
    tags = ListField(StringField(min_length=3, max_length=10))
    items_number = IntField(min_value=0)
    created_date = StringField()
    modified_date = StringField()
    owner = StringField()