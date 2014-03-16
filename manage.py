import os
import logging
import logging.config

from flask import Flask
from flask.ext.script import Manager
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api


def create_app():
    app = Flask(__name__)

    # settings
    settings_module = os.environ.get('MYHOARD_SETTINGS_MODULE')
    if not settings_module:
        raise EnvironmentError("Could not import settings, MYHOARD_SETTINGS_MODULE is None")
    app.config.from_object(settings_module)

    # mongoengine
    app.db = MongoEngine(app)

    # restful
    app.api = Api(app)

    # import urls
    with app.app_context():
        import myhoard.urls

    # logging
    logging.config.dictConfig(app.config['LOGGING'])

    logger = logging.getLogger(__name__)
    logger.info("app created")

    return app


manager = Manager(create_app)

if __name__ == "__main__":
    manager.run()