# Flask
DEBUG = False
TESTING = False

# Auth
AUTH_KEEP_ALIVE_TIME = 300
AUTH_CLASSES = ('myhoard.apps.auth.oauth.models.Token',)

# Image
MAX_CONTENT_LENGTH = 10 * 1024 * 1024 # 10MiB
IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png')
IMAGE_THUMBNAIL_SIZES = (160, 300, 340, 500)

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
            'filename': 'myHoard.log',
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
