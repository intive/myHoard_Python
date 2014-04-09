import os
import logging
import logging.config

from flask import Flask
from flask.ext.script import Manager
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api


def create_app():
    app = Flask(__name__)

    # Settings
    settings_module_name = os.environ.get('MYHOARD_SETTINGS_MODULE')
    if not settings_module_name:
        raise EnvironmentError(
            "Could not import settings, MYHOARD_SETTINGS_MODULE is None")
    app.config.from_object(settings_module_name)

    # Converters
    from myhoard.apps.common.converters import ObjectIDConverter

    app.url_map.converters['ObjectId'] = ObjectIDConverter

    # Logging
    logging.config.dictConfig(app.config['LOGGING'])

    logger = logging.getLogger(__name__)
    logger.info("app created")

    # Mongoengine
    app.db = MongoEngine(app)

    # Restful
    app.api = Api(app)

    # Errors
    from myhoard.apps.common.errors import handle_custom_errors

    app.register_error_handler(401, handle_custom_errors)  # Early errors
    app.register_error_handler(403, handle_custom_errors)  # Early errors
    app.register_error_handler(Exception, handle_custom_errors)  # Early errors
    app.api.handle_error = handle_custom_errors  # Late errors

    # Import urls
    with app.app_context():
        import myhoard.urls

    return app


manager = Manager(create_app)

if __name__ == "__main__":
    manager.run()