from flask import Flask
from flask.ext.script import Manager
from flask.ext.mongoengine import MongoEngine
from my_hoard.urls import urls

# mongoengine
db = MongoEngine()


def create_app(settings=None):
    app = Flask(__name__)
    configure_app(app, settings)
    configure_database(app)
    # register blueprints
    app.register_blueprint(urls)

    return app


def configure_app(app, settings):
    """ loading application settings """
    # map of settings
    settings_map = {
        'dev': 'my_hoard.settings.dev.DevConfig',
        'prod': 'my_hoard.settings.prod.ProdConfig',
        'test': 'my_hoard.settings.test.TestingConfig'
    }
    if settings is None or settings not in settings_map.keys():
        settings = 'dev'

    app.config.from_object(settings_map[settings])


def configure_database(app):
    """ database configuration """
    db.app = app
    db.init_app(app)


# create manager instance
manager = Manager(create_app)
manager.add_option("-s", "--settings", dest="settings", required=False)

if __name__ == "__main__":
    manager.run()