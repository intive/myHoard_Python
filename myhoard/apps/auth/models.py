from werkzeug.security import generate_password_hash
from werkzeug.exceptions import Forbidden
import logging

from flask.ext.mongoengine import Document
from mongoengine import StringField, EmailField
from flask import g

from myhoard.apps.collections.models import Collection

logger = logging.getLogger(__name__)


class User(Document):
    username = StringField()
    email = EmailField(unique=True, required=True)
    password = StringField(required=True, min_length=4)

    meta = {
        'indexes': ['email'],
    }

    def __unicode__(self):
        return '<{} {}>'.format(type(self).__name__, self.id)

    @classmethod
    def get_visible_or_404(cls, user_id):
        user = cls.objects.get_or_404(id=user_id)

        logger.debug('get_visible_or_404 dump:\nuser: {}'.format(user._data))

        return user

    @classmethod
    def create(cls, **kwargs):
        user = cls(**kwargs)
        user.id = None

        if not user.username:
            user.username = user.email

        if user.password:
            user.password = generate_password_hash(user.password)

        logger.info('Creating {}...'.format(user))
        user.save()
        logger.info('Creating {} done'.format(user))

        return user

    @classmethod
    def put(cls, user_id, **kwargs):
        user = cls.objects.get_or_404(id=user_id)
        if user.id != g.user:
            raise Forbidden('Only user can edit himself')

        update_user = cls(**kwargs)

        return cls.update(user, update_user)

    @classmethod
    def patch(cls, user_id, **kwargs):
        user = cls.objects.get_or_404(id=user_id)
        if user.id != g.user:
            raise Forbidden('Only user can edit himself')

        update_user = cls()

        for field in cls._fields:
            update_user[field] = kwargs.get(field, user[field])

        return cls.update(user, update_user)

    @classmethod
    def update(cls, user, update_user):
        update_user.id = user.id

        if not update_user.username:
            update_user.username = update_user.email

        update_user.validate()

        if user.password != update_user.password:
            update_user.password = generate_password_hash(update_user.password)

        logger.info('Updating {}...'.format(update_user))
        update_user.save(validate=False)
        logger.info('Updating {} done'.format(update_user))

        return update_user

    @classmethod
    def delete(cls, user_id):
        from myhoard.apps.auth.oauth.models import Token

        user = cls.objects.get_or_404(id=user_id)
        if g.user != user.id:
            raise Forbidden('Only user can delete himself')

        Token.delete_from_user(user)
        Collection.delete_from_user(user)

        logger.info('Deleting {}...'.format(user))
        super(cls, user).delete()
        logger.info('Deleting {} done'.format(user))