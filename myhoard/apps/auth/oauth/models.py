from uuid import uuid4
from datetime import datetime
import logging

from werkzeug.security import check_password_hash
from werkzeug.exceptions import Forbidden

from flask import current_app, g
from flask.ext.mongoengine import Document
from mongoengine import UUIDField, ObjectIdField, DateTimeField, DoesNotExist, ValidationError

from myhoard.apps.auth.models import User
from myhoard.apps.common.errors import UnauthorizedBadCredentials

logger = logging.getLogger(__name__)


class Token(Document):
    access_token = UUIDField(unique=True)
    refresh_token = UUIDField(unique=True)
    owner = ObjectIdField()
    created = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            {
                'fields': ['created'],
                'expireAfterSeconds': current_app.config['AUTH_KEEP_ALIVE_TIME']
            }
        ]
    }

    def __unicode__(self):
        return '<{} {}>'.format(type(self).__name__, self.id)

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
            user = User.objects.get(email__iexact=email)
        except DoesNotExist:
            raise UnauthorizedBadCredentials('Login failed')

        if not check_password_hash(user.password, password):
            raise UnauthorizedBadCredentials('Login failed')

        token = cls()
        token.access_token = uuid4()
        token.refresh_token = uuid4()
        token.owner = user.id

        logger.info('Creating {} ...'.format(token))
        token.save()
        logger.info('Creating {} done'.format(token))

        return token

    @classmethod
    def refresh(cls, access_token, refresh_token):
        errors = {}
        if not access_token:
            errors['access_token'] = 'Field is required'

        if not refresh_token:
            errors['refresh_token'] = 'Field is required'

        if errors:
            raise ValidationError(errors=errors)

        try:
            token = Token.objects.get(access_token=access_token, refresh_token=refresh_token)
        except (ValueError, DoesNotExist):
            raise UnauthorizedBadCredentials('Login failed')

        update_token = cls()

        return cls.update(token, update_token)

    @classmethod
    def update(cls, token, update_token):
        update_token.id = token.id
        update_token.access_token = uuid4()
        update_token.refresh_token = uuid4()
        update_token.owner = token.owner
        update_token.created = None

        logger.info('Updating {} ...'.format(update_token))
        update_token.save()
        logger.info('Updating {} done'.format(update_token))

        return update_token

    @classmethod
    def delete(cls, token_id):
        token = cls.objects.get_or_404(id=token_id)
        if token.owner != g.user:
            raise Forbidden('Only token owner can delete token')

        logger.info('Deleting {} ...'.format(token))
        super(cls, token).delete()
        logger.info('Deleting {} done'.format(token))

    @classmethod
    def delete_from_user(cls, user):
        logger.info('Deleting {} Tokens ...'.format(user))

        for token_id in cls.objects(owner=user.id).scalar('id'):
            cls.delete(token_id)

        logger.info('Deleting {} Tokens done'.format(user))