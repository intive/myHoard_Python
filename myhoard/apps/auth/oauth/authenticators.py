from werkzeug.exceptions import Forbidden

from flask import request, g
from mongoengine import DoesNotExist

from myhoard.apps.auth.authenticators import BaseAuthenticator
from myhoard.apps.common.errors import UnauthorizedNoToken, \
    UnauthorizedTokenInvalid

from models import Token


class OAuthAuthenticator(BaseAuthenticator):
    def authenticate(self):
        if 'Authorization' in request.headers:
            try:
                token = Token.objects.get(
                    access_token=request.headers.get('Authorization'))
            except DoesNotExist:
                raise Forbidden('Access token not found')
            except ValueError:
                raise UnauthorizedTokenInvalid('Invalid token')

            g.user = token.user
        else:
            raise UnauthorizedNoToken('Missing Authorization header')