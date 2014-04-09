from importlib import import_module

from flask import request
from mongoengine import ValidationError


def get_request_json():
    '''returns parsed JSON data from flask request, throws ValidationError on fail'''
    json = request.get_json(silent=True)
    if not json:
        raise ValidationError('No incoming JSON data')

    return json


def load_class(path):
    '''Dynamically loads and returns class from given path'''
    mod, cls = path.rsplit('.', 1)
    mod = import_module(mod)
    return getattr(mod, cls)


def make_order_by_for_query(params):
    '''Returns mongolike sort_by prefixed with directions from given flask params'''
    directions = {'asc': '+', 'desc': '-'}

    sort_by = params.getlist('sort_by')
    sort_direction = params.get('sort_direction')

    direction = directions.get(sort_direction, '+')
    order_by = [direction + s for s in sort_by]

    return order_by