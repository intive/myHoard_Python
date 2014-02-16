from flask import request
from mongoengine import ValidationError, NotUniqueError

from myhoard.apps.common import errors


def custom_errors(f):
    def make(code, errors=None):
        resp = {
            'error_code': code,
        }

        if errors:
            resp['errors'] = errors

        return resp, 400

    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            return make(
                errors.validation_error_code,
                e.to_dict(),
            )
        except NotUniqueError:
            return make(
                errors.duplicate_error_code,
            )

    return wrapper


def get_request_json():
    return request.get_json(force=True, silent=True) or {}