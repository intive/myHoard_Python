from functools import wraps

from flask import request

from myhoard.apps.common.errors import AuthError

import oauth

_auth_methods = [oauth]


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        found = False

        for auth_method in _auth_methods:
            if auth_method.check(request):
                auth_method.handle(request)
                found = True
                break

        if not found:
            raise AuthError(
                'ERROR_CODE_AUTH_NOT_PROVIDED',
                http_code=401
            )

        return f(*args, **kwargs)

    return wrapper