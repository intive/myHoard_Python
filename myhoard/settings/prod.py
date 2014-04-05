from common import *

DEBUG = False
MONGODB_SETTINGS = {
    'HOST': '127.0.0.1',
    'PORT': 27017,
    'DB': 'myhoard',
    'USERNAME': 'myhoard',
    'PASSWORD': 'myhoard',
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'root': {
        'level': 'NOTSET',
        'handlers': ['console', 'file'],
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': '/home/pat/logs/prod/myhoard.log',
            'mode': 'a',
            'maxBytes': 2 * 1024 * 1024, # 2MiB
            'backupCount': 64,
        },
    },

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
}