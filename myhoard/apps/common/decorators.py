from flask import current_app, request, jsonify
from mongoengine import ValidationError, NotUniqueError, DoesNotExist

from myhoard.apps.common.errors import AuthError
from myhoard.apps.auth.oauth.utils import check_token


def json_response(f):
    def wrapper(*args, **kwargs):
        data, code = f(*args, **kwargs)
        return jsonify(data), code

    return wrapper


def custom_errors(f):
    def make_formatted_response(error_code, **kwargs):
        resp = {
            'error_code': error_code,
        }

        if kwargs.get('errors'):
            resp['errors'] = kwargs.get('errors')

        return resp, kwargs.get('http_code') or 400

    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            return make_formatted_response(
                current_app.config['ERROR_CODE_VALIDATION'],
                errors=e.to_dict(),
            )
        except NotUniqueError:
            return make_formatted_response(
                current_app.config['ERROR_CODE_DUPLICATE'],
            )
        except DoesNotExist:
            return make_formatted_response(
                current_app.config['ERROR_CODE_NOT_EXIST'],
                http_code=404,
            )
        except AuthError as e:
            return make_formatted_response(
                e.error_code,
                errors=e.errors,
                http_code=e.http_code
            )

    return wrapper


def login_required(f):
    def wrapper(*args, **kwargs):
        # OAuth
        if request.headers.get('Authorization'):
            check_token(request.headers.get('Authorization'))
        else:
            raise AuthError(
                current_app.config['ERROR_CODE_AUTH_NOT_PROVIDED'],
                http_code=401
            )

        return f(*args, **kwargs)

    return wrapper