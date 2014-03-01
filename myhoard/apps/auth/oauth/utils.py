from flask import g
from mongoengine import DoesNotExist

from myhoard.apps.common.errors import AuthError

from models import Token


def check(req):
    return bool(req.headers.get('Authorization'))


def handle(req):
    try:
        token = Token.objects.get(access_token=req.headers.get('Authorization'))
    except ValueError:
        raise AuthError(
            'ERROR_CODE_AUTH_BAD_PROVIDED',
            http_code=401,
        )
    except DoesNotExist:
        raise AuthError(
            'ERROR_CODE_AUTH_FAILED',
            http_code=403,
        )

    g.user = token.user