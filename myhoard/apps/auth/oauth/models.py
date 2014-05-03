from uuid import uuid4
from datetime import datetime
import logging

from werkzeug.security import check_password_hash

from flask import current_app
from flask.ext.mongoengine import Document
from mongoengine import UUIDField, ObjectIdField, DateTimeField, \
    DoesNotExist, ValidationError

from myhoard.apps.auth.models import User
from myhoard.apps.common.errors import UnauthorizedBadCredentials

logger = logging.getLogger(__name__)


class Token(Document):
    access_token = UUIDField(unique=True)
    refresh_token = UUIDField(unique=True)
    user = ObjectIdField()
    created = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            {
                'fields': ['created'],
                'expireAfterSeconds': current_app.config['AUTH_KEEP_ALIVE_TIME']
            }
        ]
    }

    @classmethod
    def create(cls, email, password):
        errors = {}
        if not email:
            errors['email'] = 'Field is required'

        if not password:
            errors['password'] = 'Field is required'

        if errors:
            raise ValidationError(errors=errors)

        try:
            user = User.objects.get(email=email)
        except DoesNotExist:
            raise UnauthorizedBadCredentials('Login failed')

        if not check_password_hash(user.password, password):
            raise UnauthorizedBadCredentials('Login failed')

        token = cls(access_token=uuid4(), refresh_token=uuid4(), user=user.id)

        return token.save()

    @classmethod
    def refresh(cls, access_token='', refresh_token=''):
        errors = {}
        if not access_token:
            errors['access_token'] = 'Field is required'

        if not refresh_token:
            errors['refresh_token'] = 'Field is required'

        if errors:
            raise ValidationError(errors=errors)

        try:
            token = Token.objects.get(access_token=access_token,
                                      refresh_token=refresh_token)
        except (ValueError, DoesNotExist):
            raise UnauthorizedBadCredentials('Login failed')

        token.access_token = uuid4()
        token.refresh_token = uuid4()
        token.created = None

        return token.save()

    @classmethod
    def delete_user_tokens(cls, user_id):
        tokens = cls.objects(user=user_id)

        for token in tokens:
            logger.debug('deleting token... tokenID: {0}'.format(token.id))
            token.delete()
