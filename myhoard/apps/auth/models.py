from werkzeug.security import generate_password_hash

from flask.ext.mongoengine import Document
from mongoengine import StringField, EmailField


class User(Document):
    username = StringField()
    email = EmailField(unique=True, required=True)
    password = StringField(required=True, min_length=4)

    meta = {
        'indexes': ['email'],
    }

    @classmethod
    def create_user(cls, **kwargs):
        user = cls(**kwargs)
        user.id = None

        if not user.username:
            user.username = user.email

        if user.password:
            user.password = generate_password_hash(user.password)

        return user.save()