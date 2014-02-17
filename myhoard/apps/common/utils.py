from flask import request


def get_request_json():
    return request.get_json(force=True, silent=True) or {}