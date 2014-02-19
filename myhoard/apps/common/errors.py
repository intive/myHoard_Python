class AuthError(Exception):
    def __init__(self, error_code, **kwargs):
        self.error_code = error_code
        self.errors = kwargs.get('errors')
        self.http_code = kwargs.get('http_code')