from importlib import import_module

from flask import request
from mongoengine import ValidationError


def get_request_json():
    json = request.get_json(silent=True)
    if not json:
        raise ValidationError('No incoming JSON data')

    return json


def load_class(path):
    mod, cls = path.rsplit('.', 1)
    mod = import_module(mod)
    return getattr(mod, cls)