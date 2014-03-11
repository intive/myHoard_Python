# -*- coding: utf-8 -*-
from werkzeug.contrib.fixers import ProxyFix
import manage

__author__ = 'mkr'

myhoard = manage.create_app()

myhoard.wsgi_app = ProxyFix(myhoard.wsgi_app)

if __name__ == '__main__':
    myhoard.run()