from functools import wraps

from flask import current_app, jsonify
from mongoengine import ValidationError, NotUniqueError, DoesNotExist
from bson.errors import InvalidId

from myhoard.apps.common.errors import FileError, JSONError, AuthError


def json_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data, code = f(*args, **kwargs)
        return jsonify(data), code

    return wrapper


def custom_errors(f):
    def make_formatted_response(error_code, errors=None, http_code=400):
        resp = {
            'error_code': current_app.config[error_code],
            'error_message': error_code,
        }

        if errors:
            resp['errors'] = errors

        return resp, http_code

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except FileError as e:
            return make_formatted_response(
                e.error_code,
                errors=e.errors,
            )
        except JSONError:
            return make_formatted_response(
                'ERROR_CODE_NO_INCOMING_JSON_DATA',
            )
        except ValidationError as e:
            return make_formatted_response(
                'ERROR_CODE_VALIDATION',
                errors=e.to_dict(),
            )
        except NotUniqueError:
            return make_formatted_response(
                'ERROR_CODE_DUPLICATE',
            )
        except DoesNotExist:
            return make_formatted_response(
                'ERROR_CODE_NOT_EXIST',
                http_code=404,
            )
        except AuthError as e:
            return make_formatted_response(
                e.error_code,
                errors=e.errors,
                http_code=e.http_code,
            )
        # raised when trying to get Object with an invalid id.
        except InvalidId as e:
            return make_formatted_response(
                'ERROR_CODE_NOT_EXIST',
                errors={'ObjectId': str(e)},
                http_code=404,
            )

    return wrapper