from common import Config


class ProdConfig(Config):
    MONGODB_SETTINGS = {'DB': "'mongo_db_prod'"}