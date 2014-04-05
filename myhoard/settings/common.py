# Flask
DEBUG = False
TESTING = False

# Auth
AUTH_KEEP_ALIVE_TIME = 300
AUTH_CLASSES = ('myhoard.apps.auth.oauth.authenticators.OAuthAuthenticator',)

# Image
MAX_CONTENT_LENGTH = 10 * 1024 * 1024 # 10MiB
IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png')
IMAGE_THUMBNAIL_SIZES = (160, 300, 340, 500)

