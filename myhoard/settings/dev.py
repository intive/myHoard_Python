from common import *

DEBUG = True
MONGODB_SETTINGS = {
    'HOST': '127.0.0.1',
    'PORT': 27017,
    'DB': 'myhoard_dev',
    'USERNAME': 'myhoard',
    'PASSWORD': 'myh0@rd',
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
            'filename': '/home/pat/logs/dev/myhoard.log',
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