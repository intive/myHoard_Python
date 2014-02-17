from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph


def generate_password_hash(password):
    return gph(password)


def check_password_hash(password):
    return cph(password)