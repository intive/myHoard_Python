from flask import Flask
from flask.ext.script import Manager
from flask.ext.mongoengine import MongoEngine
import os


def create_app():
    app = Flask(__name__)
    # settings
    settings_module = os.environ.get('MYHOARD_SETTINGS_MODULE')
    app.config.from_object(settings_module)
    # mongoengine
    db = MongoEngine()
    db.init_app(app)
    # import urls
    with app.app_context():
        import myhoard.urls

    return app


manager = Manager(create_app)

if __name__ == "__main__":
    manager.run()