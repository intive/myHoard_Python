from werkzeug.exceptions import Forbidden
from datetime import datetime
import logging

from flask import g
from flask.ext.mongoengine import Document
from mongoengine import StringField, ObjectIdField, DateTimeField
from myhoard.apps.collections.models import Collection

logger = logging.getLogger(__name__)


class Comment(Document):
    content = StringField(min_length=1, max_length=160, required=True)
    created_date = DateTimeField(default=datetime.now)
    collection = ObjectIdField(required=True)
    owner = ObjectIdField()

    def __repr__(self):
        return '<Comment {}>'.format(self.content)

    @classmethod
    def create(cls, **kwargs):
        comment = cls(**kwargs)
        comment.created_date = None
        comment.owner = g.user
        comment.save()

        logger.debug('comment with id: {} created'.format(comment.id))

        return comment

    @classmethod
    def delete_(cls, comment_id):
        comment = cls.objects.get_or_404(id=comment_id)
        collection = Collection.objects.get_or_404(id=comment.collection)
        if g.user != comment.owner or g.user != collection.owner:
            logger.debug(
                'current user does not have permission to remove comment with id: {}'.format(
                    comment_id))
            raise Forbidden(
                'Only comment or collection owner can delete comments')

        return comment.delete()
