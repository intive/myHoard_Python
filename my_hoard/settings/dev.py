from common import Config


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {'DB': "mongo_db_dev"}