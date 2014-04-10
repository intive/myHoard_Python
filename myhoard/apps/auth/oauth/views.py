from flask import current_app
from flask.ext.restful import fields, marshal, marshal_with
from mongoengine import ValidationError

from myhoard.apps.auth.decorators import login_required
from myhoard.apps.common.utils import get_request_json
from myhoard.apps.common.decorators import json_response

from models import Token

token_fields = {
    'access_token': fields.String,
    'expires_in': fields.Integer(current_app.config['AUTH_KEEP_ALIVE_TIME']),
    'refresh_token': fields.String,
    'user_id': fields.String(attribute='user'),
}


@json_response
def oauth():
    args = get_request_json()

    if 'grant_type' not in args:
        raise ValidationError(errors={'grant_type': 'Field is required'})

    if args.get('grant_type') == 'password':
        return marshal(
            Token.create(args.get('email'), args.get('password')),
            token_fields), 200
    elif args.get('grant_type') == 'refresh_token':
        return login_required(marshal_with(token_fields)(Token.refresh))(
            args.get('access_token'), args.get('refresh_token')), 200
    else:
        raise ValidationError(errors={'grant_type': 'Unsupported grant_type'})