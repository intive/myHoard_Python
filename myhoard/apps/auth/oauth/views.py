from uuid import uuid4

from werkzeug.security import check_password_hash
from flask import request, current_app
from mongoengine import DoesNotExist

from myhoard.apps.auth.models import User
from myhoard.apps.auth.decorators import login_required
from myhoard.apps.common.decorators import json_response, custom_errors
from myhoard.apps.common.errors import AuthError

from models import Token


def create_token(**kwargs):
    try:
        user = User.objects.get(username=kwargs.get('username', ''))
    except DoesNotExist:
        raise AuthError('ERROR_CODE_AUTH_FAILED')

    if not check_password_hash(user.password, kwargs.get('password', '')):
        raise AuthError('ERROR_CODE_AUTH_FAILED')

    token = Token(
        access_token=uuid4(),
        refresh_token=uuid4(),
        user=user.id,
    )
    token.save()

    return {
               'access_token': token.access_token,
               'expires_in': current_app.config['AUTH_KEEP_ALIVE_TIME'],
               'refresh_token': token.refresh_token,
           }, 200


@login_required
def refresh_token(**kwargs):
    try:
        token = Token.objects.get(refresh_token=kwargs.get('refresh_token', ''))
    except (ValueError, DoesNotExist):
        raise AuthError(
            'ERROR_CODE_AUTH_FAILED',
        )

    token.access_token = uuid4()
    token.refresh_token = uuid4()
    token.created = None
    token.save()

    return {
               'access_token': token.access_token,
               'expires_in': current_app.config['AUTH_KEEP_ALIVE_TIME'],
               'refresh_token': token.refresh_token,
           }, 200


@json_response
@custom_errors
def oauth():
    args = request.form.to_dict()

    if args.get('grant_type') == 'password':
        return create_token(**args)
    elif args.get('grant_type') == 'refresh_token':
        return refresh_token(**args)
    else:
        raise AuthError(
            'ERROR_CODE_AUTH',
            errors={'grant_type': 'Unsupported grant_type'},
        )