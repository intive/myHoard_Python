from flask import current_app
from mongoengine import ValidationError, NotUniqueError


def custom_errors(f):
    def make_formated_response(code, errors=None):
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
            return make_formated_response(
                current_app.config['ERROR_CODE_VALIDATION'],
                e.to_dict(),
            )
        except NotUniqueError:
            return make_formated_response(
                current_app.config['ERROR_CODE_DUPLICATE'],
            )

    return wrapper