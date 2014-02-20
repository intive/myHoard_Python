# -*- coding: utf-8 -*-
from werkzeug.contrib.fixers import ProxyFix
import manage

__author__ = 'mkr'

app = manage.create_app()

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()