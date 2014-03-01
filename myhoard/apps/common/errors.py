class JSONError(Exception):
    pass


class AuthError(Exception):
    def __init__(self, error_code, errors=None, http_code=None):
        self.error_code = error_code
        self.errors = errors
        self.http_code = http_code