import logging
from datetime import datetime

from werkzeug.exceptions import Forbidden, NotFound

from flask import g
from flask.ext.mongoengine import Document
from mongoengine import StringField, ListField, ObjectIdField, DateTimeField, PointField

from myhoard.apps.media.models import Media
from myhoard.apps.common.utils import make_order_by_for_query, make_item_search_query

logger = logging.getLogger(__name__)


class Item(Document):
    name = StringField(min_length=3, max_length=50, required=True)
    description = StringField(max_length=250, default='')
    location = PointField()
    created_date = DateTimeField(default=datetime.now)
    modified_date = DateTimeField(default=datetime.now)
    media = ListField(ObjectIdField())
    collection = ObjectIdField(required=True)
    owner = ObjectIdField()

    @property
    def public(self):
        from myhoard.apps.collections.models import Collection

        return bool(Collection.objects(id=self.collection, public=True).count())

    def __unicode__(self):
        return '<{} {}>'.format(type(self).__name__, self.id)

    @classmethod
    def get_visible_or_404(cls, item_id):
        from myhoard.apps.collections.models import Collection

        item = cls.objects.get_or_404(id=item_id)
        Collection.get_visible_or_404(item.collection)

        logger.debug('get_visible_or_404 dump:\nitem: {}'.format(getattr(item, '_data')))

        return item

    @classmethod
    def get_all(cls, params, collection_id):
        return cls.objects(make_item_search_query(params, collection_id)).order_by(*make_order_by_for_query(params))

    @classmethod
    def create(cls, **kwargs):
        from myhoard.apps.collections.models import Collection

        Collection.get_visible_or_404(kwargs.get('collection'))

        item = cls(**kwargs)
        item.id = None
        item.created_date = None
        item.modified_date = None
        item.owner = g.user

        if 'location' in item:
            item.location = {
                'type': 'Point',
                'coordinates': [item.location.get('lng'), item.location.get('lat')]
            }

        logger.info('Creating {} ...'.format(item))
        item.save()
        logger.info('Creating {} done'.format(item))

        Media.create_from_item(item)

        return item

    @classmethod
    def put(cls, item_id, **kwargs):
        item = cls.objects.get_or_404(id=item_id)
        if item.owner != g.user:
            raise Forbidden('Only collection owner can edit items') if item.public else NotFound()

        update_item = cls(**kwargs)

        return cls.update(item, update_item)

    @classmethod
    def patch(cls, item_id, **kwargs):
        item = cls.objects.get_or_404(id=item_id)
        if item.owner != g.user:
            raise Forbidden('Only collection owner can edit items') if item.public else NotFound()

        update_item = cls()

        for field in cls._fields:
            update_item[field] = kwargs.get(field, item[field])

        return cls.update(item, update_item)

    @classmethod
    def update(cls, item, update_item):
        update_item.id = item.id
        update_item.created_date = item.created_date
        update_item.modified_date = None
        update_item.owner = g.user

        if 'location' in update_item:
            update_item.location = {
                'type': 'Point',
                'coordinates': [update_item.location.get('lng'), update_item.location.get('lat')]
            }

        update_item.save()
        logger.info('{} updated'.format(item))

        return update_item

    @classmethod
    def delete(cls, item_id):
        item = cls.objects.get_or_404(id=item_id)
        if item.owner != g.user:
            raise Forbidden('Only collection owner can delete items') if item.public else NotFound()

        logger.info('Deleting {} Media'.format(item))
        Media.delete_from_item(item)

        super(cls, item).delete()
        logger.info('{} deleted'.format(item))

    @classmethod
    def delete_from_collection(cls, collection):
        logger.info('Deleting {} Items ...'.format(collection))

        for item_id in cls.objects(collection=collection.id).scalar('id'):
            cls.delete(item_id)

        logger.info('Deleting {} Items done'.format(collection))