from werkzeug.exceptions import Forbidden
from datetime import datetime
import logging

from flask import g
from flask.ext.mongoengine import Document
from mongoengine import StringField, ObjectIdField, DateTimeField
from myhoard.apps.collections.models import Collection

logger = logging.getLogger(__name__)


class Comment(Document):
    body = StringField(min_length=1, max_length=160, required=True)
    created_date = DateTimeField(default=datetime.now)
    modified_date = DateTimeField(default=datetime.now)
    collection = ObjectIdField(required=True)
    owner = ObjectIdField()

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

    @classmethod
    def create(cls, **kwargs):
        comment = cls(**kwargs)
        comment.created_date = None
        comment.modified_date = None
        comment.owner = g.user
        comment.save()

        return comment

    @classmethod
    def update(cls, comment_id, **kwargs):
        comment = cls.objects.get_or_404(id=comment_id, owner=g.user)
        update_comment = cls(**kwargs)
        comment.body = update_comment.body
        comment.modified_date = None

        return comment.save()

    @classmethod
    def remove(cls, comment_id):
        comment = cls.objects.get_or_404(id=comment_id)
        collection = Collection.objects.get_or_404(id=comment.collection)
        if g.user != comment.owner or g.user != collection.owner:
            logger.info("User does not have permission to remove this comment")
            raise Forbidden()

        return comment.delete()
