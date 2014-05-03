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

    @classmethod
    def create(cls, **kwargs):
        user = cls(**kwargs)
        user.id = None

        if not user.username:
            user.username = user.email

        if user.password:
            user.password = generate_password_hash(user.password)

        return user.save()

    @classmethod
    def put(cls, user_id, **kwargs):
        user = cls.objects.get_or_404(id=user_id)
        update_user = cls(**kwargs)

        return cls.update(user, update_user)

    @classmethod
    def patch(cls, user_id, **kwargs):
        user = cls.objects.get_or_404(id=user_id)
        update_user = cls()

        for field in user._fields:
            update_user[field] = kwargs.get(field, user[field])

        return cls.update(user, update_user)

    @classmethod
    def update(cls, user, update_user):
        update_user.id = user.id

        if not update_user.username:
            update_user.username = update_user.email

        if update_user.password:
            update_user.password = generate_password_hash(user.password)

        return update_user.save()

    @classmethod
    def delete(cls, user_id):
        user = cls.objects.get_or_404(id=user_id)
        if g.user != user.id:
            logger.info('user does not have permission to remove other user')
            raise Forbidden()

        logger.debug('deleting user collections')
        Collection.delete_by_user(user.id)

        logger.debug('deleting user tokens')
        from myhoard.apps.auth.oauth.models import Token

        Token.delete_user_tokens(user.id)

        logger.debug('deleting user')
        return super(cls, user).delete()