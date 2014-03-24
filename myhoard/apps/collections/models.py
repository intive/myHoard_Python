from datetime import datetime

from flask import g
from flask.ext.mongoengine import Document
from mongoengine import StringField, ListField, ObjectIdField, \
    DateTimeField

from items.models import Item
from myhoard.apps.common.utils import make_order_by_for_query


class Collection(Document):
    name = StringField(min_length=3, max_length=20, required=True,
                       unique_with='owner')
    description = StringField(default='')
    tags = ListField(StringField(min_length=3, max_length=20))
    created_date = DateTimeField(default=datetime.now)
    modified_date = DateTimeField(default=datetime.now)
    owner = ObjectIdField()

    def __repr__(self):
        return '<Collection {}>'.format(self.name)

    @property
    def items_count(self):
        if self.id:
            return Item.objects(collection=self.id).count()
        else:
            return 0

    @classmethod
    def create_collection(cls, **kwargs):
        collection = cls(**kwargs)
        collection.id = None
        collection.owner = g.user
        collection.created_date = None
        collection.modified_date = None

        return collection.save()

    @classmethod
    def update_collection(cls, collection_id, **kwargs):
        collection = cls.objects.get_or_404(id=collection_id)
        update_collection = cls(**kwargs)
        update_collection.id = collection.id
        update_collection.created_date = collection.created_date
        update_collection.modified_date = None
        update_collection.owner = collection.owner

        return update_collection.save()

    @classmethod
    def delete_collection(cls, collection_id):
        collection = cls.objects.get_or_404(id=collection_id)
        Item.delete_collection_items(collection)

        return collection.delete()

    @classmethod
    def get_ordered(cls, params):

        return cls.objects(owner=g.user).order_by(*make_order_by_for_query(params))
