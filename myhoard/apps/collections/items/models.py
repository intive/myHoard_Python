from datetime import datetime

from flask import g
from flask.ext.mongoengine import Document
from mongoengine import StringField, ListField, ObjectIdField, DateTimeField, \
    GeoPointField

from myhoard.apps.media.models import Media
from myhoard.apps.common.utils import make_order_by_for_query


class Item(Document):
    name = StringField(min_length=3, max_length=50, required=True)
    description = StringField(max_length=250, default='')
    location = GeoPointField()
    created_date = DateTimeField(default=datetime.now)
    modified_date = DateTimeField(default=datetime.now)
    media = ListField(ObjectIdField())
    collection = ObjectIdField(required=True)
    owner = ObjectIdField()

    def __repr__(self):
        return '<Item {}>'.format(self.name)

    @classmethod
    def create(cls, **kwargs):
        item = cls(**kwargs)
        item.id = None
        item.created_date = None
        item.modified_date = None
        item.owner = g.user

        if 'location' in item:
            item.location = (item.location.get('lat'), item.location.get('lng'))

        item.save()

        Media.create_from_item(item)

        return item

    @classmethod
    def update(cls, item_id, **kwargs):
        item = cls.objects.get_or_404(id=item_id, owner=g.user)
        update_item = cls(**kwargs)
        update_item.id = item.id
        update_item.created_date = item.created_date
        update_item.modified_date = None

        Media.update_from_item(item, update_item)

        return update_item.save()

    @classmethod
    def delete_(cls, item_id):
        item = cls.objects.get_or_404(id=item_id, owner=g.user)

        Media.delete_from_item(item)

        return item.delete()

    @classmethod
    def delete_from_collection(cls, collection):
        for item in cls.objects(collection=collection.id):
            Media.delete_from_item(item)

            item.delete()

    @classmethod
    def get_ordered(cls, params, collection_id):
        return cls.objects(owner=g.user, collection=collection_id).order_by(
            *make_order_by_for_query(params))