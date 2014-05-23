import logging
from datetime import datetime

from werkzeug.exceptions import Forbidden, NotFound

from flask import g
from flask.ext.mongoengine import Document
from mongoengine import StringField, ObjectIdField, DateTimeField, ValidationError

logger = logging.getLogger(__name__)


class Comment(Document):
    content = StringField(min_length=1, max_length=160, required=True)
    created_date = DateTimeField(default=datetime.now)
    collection = ObjectIdField(required=True)
    owner = ObjectIdField()

    @property
    def public(self):
        from myhoard.apps.collections.models import Collection

        return bool(Collection.objects(id=self.collection, public=True).count())

    def __unicode__(self):
        return '<{} {}>'.format(type(self).__name__, self.id)

    @classmethod
    def get_public_or_404(cls, comment_id):
        from myhoard.apps.collections.models import Collection

        comment = cls.objects.get_or_404(id=comment_id)
        Collection.get_visible_or_404(comment.collection)

        logger.debug('get_visible_or_404 dump:\ncomment: {}'.format(getattr(comment, '_data')))

        return comment

    @classmethod
    def create(cls, **kwargs):
        from myhoard.apps.collections.models import Collection

        try:
            Collection.get_visible_or_404(kwargs.get('collection'))
        except NotFound:
            raise ValidationError(errors={'collection': 'Not found'})

        comment = cls(**kwargs)
        comment.created_date = None
        comment.owner = g.user

        logger.info('Creating {} ...'.format(comment))
        comment.save()
        logger.info('Creating {} done'.format(comment))

        return comment

    @classmethod
    def delete(cls, comment_id):
        from myhoard.apps.collections.models import Collection

        comment = cls.objects.get_or_404(id=comment_id)
        collection = Collection.objects.get_or_404(id=comment.collection)
        if (g.user != comment.owner) or (g.user != collection.owner):
            raise Forbidden('Only comment or collection owner can delete comment')

        logger.info('Deleting {} ...'.format(comment))
        super(cls, comment).delete()
        logger.info('Deleting {} done'.format(comment))

    @classmethod
    def delete_from_collection(cls, collection):
        logger.info('Deleting {} Comments ...'.format(collection))

        for comment_id in cls.objects(collection=collection.id).scalar('id'):
            cls.delete(comment_id)

        logger.info('Deleting {} Comments done'.format(collection))