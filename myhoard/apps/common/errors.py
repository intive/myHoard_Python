import logging
import re

from werkzeug.exceptions import Unauthorized, Forbidden, NotFound

from mongoengine import ValidationError, NotUniqueError

from decorators import json_response

logger = logging.getLogger(__name__)


class UnauthorizedBadCredentials(Unauthorized):
    pass


class UnauthorizedNoToken(Unauthorized):
    pass


class UnauthorizedTokenInvalid(Unauthorized):
    pass


_custom_error_mapping = {
    #error_code, http_code, error_message
    UnauthorizedBadCredentials: (101, 401, 'Bad credentials'),
    UnauthorizedNoToken: (102, 401, 'Token not provided'),
    UnauthorizedTokenInvalid: (103, 401, 'Invalid token'),
    Forbidden: (104, 403, 'Forbidden'),
    ValidationError: (201, 400, 'Validation error'),
    NotUniqueError: (201, 400, 'Validation error'),
    NotFound: (202, 404, 'Resource not found'),
}

_duplicate_re = re.compile(r'\$(.+?)_')


@json_response
def handle_custom_errors(e):
    error_type = type(e)
    if error_type in _custom_error_mapping:
        logger.debug(e) # just typical exception to handle

        error_code, http_code, error_message = _custom_error_mapping[error_type]

        resp = {
            'error_code': error_code,
            'error_message': error_message,
        }

        if isinstance(e, ValidationError):
            errors = e.to_dict()
            if errors:
                resp['errors'] = errors
            else:
                resp['error_message'] = e.message

        if isinstance(e, NotUniqueError):
            resp['errors'] = {}
            fields = _duplicate_re.findall(e.message)

            for field in fields:
                resp['errors'][field] = 'Duplicate value'

        return resp, http_code
    else:
        logger.exception(e) # everything is on fire, panic is only solution

        return {
                   'error_code': 301,
                   'error_message': 'Unexpected server exception: {}'.format(e),
               }, 500