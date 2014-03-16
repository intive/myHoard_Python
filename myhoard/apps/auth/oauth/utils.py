from flask import g
from mongoengine import DoesNotExist
import logging

from myhoard.apps.common.errors import AuthError

from models import Token

logger = logging.getLogger(__name__)

def check(req):
    return bool(req.headers.get('Authorization'))


def handle(req):
    try:
        token = Token.objects.get(access_token=req.headers.get('Authorization'))
    except ValueError as e:
        logger.exception(e)
        raise AuthError(
            'ERROR_CODE_AUTH_BAD_PROVIDED',
            http_code=401,
        )
    except DoesNotExist as e:
        logger.exception(e)
        raise AuthError(
            'ERROR_CODE_AUTH_FAILED',
            http_code=403,
        )

    g.user = token.user