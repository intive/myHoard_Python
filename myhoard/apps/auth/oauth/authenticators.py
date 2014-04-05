from werkzeug.exceptions import Unauthorized, Forbidden

from flask import request, g
from mongoengine import DoesNotExist

from myhoard.apps.auth.authenticators import BaseAuthenticator

from models import Token


class OAuthAuthenticator(BaseAuthenticator):
    def authenticate(self):
        if 'Authorization' in request.headers:
            try:
                token = Token.objects.get(
                    access_token=request.headers.get('Authorization'))
            except (ValueError, DoesNotExist):
                # TODO Why value error?
                # TODO missing logs
                # TODO add error message
                raise Forbidden()

            g.user = token.user
        else:
            # TODO missing logs
            # TODO add error message
            raise Unauthorized()