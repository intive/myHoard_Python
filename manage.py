from flask import Flask
from flask.ext.script import Manager
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api
import os


def create_app():
    app = Flask(__name__)

    # settings
    settings_module = os.environ.get('MYHOARD_SETTINGS_MODULE')
    if settings_module is None:
        raise EnvironmentError("Could not import settings, MYHOARD_SETTINGS_MODULE is None")
    app.config.from_object(settings_module)

    # mongoengine
    app.db = MongoEngine(app)

    # restful
    app.api = Api(app)

    # import urls
    with app.app_context():
        import myhoard.urls

    return app


manager = Manager(create_app)

if __name__ == "__main__":
    manager.run()