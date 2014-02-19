from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
from flask import current_app, g
from mongoengine import DoesNotExist

from myhoard.apps.common.errors import AuthError

from models import Token


def generate_password_hash(password):
    return gph(password)


def check_password_hash(hash, password):
    return cph(hash, password)


def check_token(token):
    try:
        token = Token.objects.get(access_token=token)
    except (ValueError, DoesNotExist):
        raise AuthError(
            current_app.config['ERROR_CODE_AUTH_REQUIRED'],
            http_code=403,
        )

    g.user = token.user