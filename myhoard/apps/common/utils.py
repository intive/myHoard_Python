from flask import request

from myhoard.apps.common.errors import JSONError


def get_request_json():
    json = request.get_json(silent=True)
    if not json:
        raise JSONError()

    return json