from functools import wraps

from flask import current_app

from myhoard.apps.common.utils import load_class

_auth_classes = []


def _load_auth_classes():
    for auth_class in current_app.config['AUTH_CLASSES']:
        _auth_classes.append(load_class(auth_class)())


_load_auth_classes()
del _load_auth_classes


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        for auth_class in _auth_classes:
            auth_class.authenticate()

        return f(*args, **kwargs)

    return wrapper