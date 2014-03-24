from functools import wraps
from json import dumps

from flask import Response


def json_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data, code = f(*args, **kwargs)
        return Response(dumps(data), mimetype='application/json'), code

    return wrapper