from common import Config


class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {'DB': "'mongo_db_test'"}