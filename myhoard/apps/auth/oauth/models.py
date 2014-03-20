from datetime import datetime

from flask import current_app
from mongoengine import Document, UUIDField, StringField, ObjectIdField, \
    DateTimeField


class Token(Document):
    # TODO Rememeber - Fat models, thin views
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