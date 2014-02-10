from flask import Flask
from flask.ext.script import Manager
from flask.ext.mongoengine import MongoEngine
from myhoard.urls import urls
import os


def create_app():
    app = Flask(__name__)
    # settings
    settings_module = os.environ.get('MYHOARD_SETTINGS_MODULE')
    app.config.from_object(settings_module)
    # mongoengine
    db = MongoEngine()
    db.init_app(app)

    # TODO import urls, remove blueprint
    app.register_blueprint(urls)
    return app


manager = Manager(create_app)

if __name__ == "__main__":
    manager.run()