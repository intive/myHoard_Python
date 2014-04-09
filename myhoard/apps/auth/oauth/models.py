from uuid import uuid4
from datetime import datetime

from werkzeug.security import check_password_hash
from werkzeug.exceptions import Forbidden

from flask import current_app
from flask.ext.mongoengine import Document
from mongoengine import UUIDField, ObjectIdField, DateTimeField, \
    DoesNotExist

from myhoard.apps.auth.models import User


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
    def create(cls, email='', password=''):
        try:
            user = User.objects.get(email=email)
        except DoesNotExist:
            raise Forbidden()

        if not check_password_hash(user.password, password):
            raise Forbidden()

        token = cls(access_token=uuid4(), refresh_token=uuid4(), user=user.id)

        return token.save()

    @classmethod
    def refresh(cls, access_token='', refresh_token=''):
        try:
            token = Token.objects.get(access_token=access_token,
                                      refresh_token=refresh_token)
        except (ValueError, DoesNotExist):
            raise Forbidden()

        token.access_token = uuid4()
        token.refresh_token = uuid4()
        token.created = None

        return token.save()