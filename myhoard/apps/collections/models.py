from mongoengine import Document, StringField, ListField, IntField


class Collection(Document):
    name = StringField(max_length=20, required=True)
    description = StringField(max_length=50, required=True)
    tags = ListField(StringField())
    items_number = IntField(min_value=0)
    created_date = StringField()
    modified_date = StringField()
    owner = StringField()