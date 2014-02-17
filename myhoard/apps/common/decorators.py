from flask import current_app
from mongoengine import ValidationError, NotUniqueError, DoesNotExist
 
 
def custom_errors(f):
    def make_formated_response(error_code, http_code, errors=None):
        resp = {
            'error_code': error_code,
        }
 
        if errors:
            resp['errors'] = errors
 
        return resp, http_code
 
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            return make_formated_response(
                current_app.config['ERROR_CODE_VALIDATION'],
                400,
                e.to_dict(),
            )
        except NotUniqueError:
            return make_formated_response(
                current_app.config['ERROR_CODE_DUPLICATE'],
                400,
            )
        except DoesNotExist:
            return make_formated_response(
                current_app.config['ERROR_CODE_NOT_EXIST'],
                404,
            )
 
    return wrapper