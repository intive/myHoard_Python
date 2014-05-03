from datetime import datetime
import logging

from flask import g
from flask.ext.mongoengine import Document
from mongoengine import StringField, ListField, ObjectIdField, \
    DateTimeField, BooleanField

from myhoard.apps.common.utils import make_order_by_for_query, \
    make_collection_search_query

from items.models import Item

logger = logging.getLogger(__name__)


class Collection(Document):
    name = StringField(min_length=3, max_length=20, required=True,
                       unique_with='owner')
    description = StringField(default='')
    tags = ListField(StringField(min_length=3, max_length=20))
    created_date = DateTimeField(default=datetime.now)
    modified_date = DateTimeField(default=datetime.now)
    owner = ObjectIdField()
    public = BooleanField(default=False)

    def __repr__(self):
        return '<Collection {}>'.format(self.name)

    @property
    def items_count(self):
        return Item.objects(collection=self.id).count() if self.id else 0

    @classmethod
    def create(cls, **kwargs):
        collection = cls(**kwargs)
        collection.id = None
        collection.created_date = None
        collection.modified_date = None
        collection.owner = g.user

        return collection.save()

    @classmethod
    def put(cls, collection_id, **kwargs):
        collection = cls.objects.get_or_404(id=collection_id, owner=g.user)
        update_collection = cls(**kwargs)

        return cls.update(collection, update_collection)

    @classmethod
    def patch(cls, collection_id, **kwargs):
        collection = cls.objects.get_or_404(id=collection_id, owner=g.user)
        update_collection = cls()

        for field in collection._fields:
            update_collection[field] = kwargs.get(field, collection[field])

        return cls.update(collection, update_collection)

    @classmethod
    def update(cls, collection, update_collection):
        update_collection.id = collection.id
        update_collection.created_date = collection.created_date
        update_collection.modified_date = None
        update_collection.owner = collection.owner

        return super(cls, update_collection).save()

    @classmethod
    def delete(cls, collection_id):
        collection = cls.objects.get_or_404(id=collection_id, owner=g.user)

        super(cls, collection).delete()
        Item.delete_from_collection(collection)

        return collection

    @classmethod
    def delete_by_user(cls, user_id):
        for collection in cls.objects(owner=user_id):
            logger.debug(
                'deleting collection... collectionID: {} collection name: {}'
                .format(collection.id, collection.name))
            collection.delete(collection.id)

    @classmethod
    def get_all(cls, params):
        return cls.objects(make_collection_search_query(params)).order_by(
            *make_order_by_for_query(params))
