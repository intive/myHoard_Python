import logging
from datetime import datetime

from werkzeug.exceptions import Forbidden, NotFound

from flask import g
from flask.ext.mongoengine import Document
from mongoengine import Q, StringField, ListField, ObjectIdField, DateTimeField, BooleanField

from myhoard.apps.common.utils import make_order_by_for_query, make_collection_search_query

from items.models import Item
from comments.models import Comment

logger = logging.getLogger(__name__)


class Collection(Document):
    name = StringField(min_length=3, max_length=20, required=True, unique_with='owner')
    description = StringField(default='')
    tags = ListField(StringField(min_length=3, max_length=20))
    created_date = DateTimeField(default=datetime.now)
    modified_date = DateTimeField(default=datetime.now)
    owner = ObjectIdField()
    public = BooleanField(default=False)

    @property
    def items_count(self):
        return Item.objects(collection=self.id).count() if self.id else 0

    def __unicode__(self):
        return '<{} {}>'.format(type(self).__name__, self.id)

    @classmethod
    def get_visible_or_404(cls, collection_id):
        collection = Collection.objects.get_or_404(Q(id=collection_id) & (Q(owner=g.user) | Q(public=True)))

        logger.debug('get_visible_or_404 dump:\ncollection: {}'.format(collection._data))

        return collection

    @classmethod
    def get_all(cls, params):
        return cls.objects(make_collection_search_query(params)).order_by(
            *make_order_by_for_query(params))

    @classmethod
    def create(cls, **kwargs):
        collection = cls(**kwargs)
        collection.id = None
        collection.created_date = None
        collection.modified_date = None
        collection.owner = g.user

        logger.info('Creating {}...'.format(collection))
        collection.save()
        logger.info('Creating {} done'.format(collection))

        return collection

    @classmethod
    def put(cls, collection_id, **kwargs):
        collection = cls.objects.get_or_404(id=collection_id)
        if collection.owner != g.user:
            raise Forbidden('Only collection owner can edit collection') if collection.public else NotFound()

        update_collection = cls(**kwargs)

        return cls.update(collection, update_collection)

    @classmethod
    def patch(cls, collection_id, **kwargs):
        collection = cls.objects.get_or_404(id=collection_id)
        if collection.owner != g.user:
            raise Forbidden('Only collection owner can edit collection') if collection.public else NotFound()

        update_collection = cls()

        for field in cls._fields:
            update_collection[field] = kwargs.get(field, collection[field])

        return cls.update(collection, update_collection)

    @classmethod
    def update(cls, collection, update_collection):
        update_collection.id = collection.id
        update_collection.created_date = collection.created_date
        update_collection.modified_date = None
        update_collection.owner = collection.owner

        logger.info('Updating {}...'.format(update_collection))
        super(cls, update_collection).save()
        logger.info('Updating {} done'.format(update_collection))

        return update_collection

    @classmethod
    def delete(cls, collection_id):
        collection = cls.objects.get_or_404(id=collection_id)
        if collection.owner != g.user:
            raise Forbidden('Only collection owner can delete collection') if collection.public else NotFound()

        Comment.delete_from_collection(collection)
        Item.delete_from_collection(collection)

        logger.info('Deleting {}...'.format(collection))
        super(cls, collection).delete()
        logger.info('Deleting {} done'.format(collection))

    @classmethod
    def delete_from_user(cls, user):
        logger.info('Deleting {} Collections...'.format(user))

        for collection_id in cls.objects(owner=user.id).scalar('id'):
            cls.delete(collection_id)

        logger.info('Deleting {} Collections done'.format(user))