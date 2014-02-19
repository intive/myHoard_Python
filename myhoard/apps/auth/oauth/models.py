from datetime import datetime

from flask import current_app
from mongoengine import Document, UUIDField, StringField, ObjectIdField, \
    DateTimeField


class Token(Document):
    access_token = UUIDField(unique=True)
    refresh_token = UUIDField(unique=True)
    user = ObjectIdField()
    scope = StringField(choices=('read', 'write', 'read+write'))
    created = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            {
                'fields': ['created'],
                'expireAfterSeconds': current_app.config['AUTH_KEEP_ALIVE_TIME']
            }
        ]
    }