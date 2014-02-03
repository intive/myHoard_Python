from flask.ext.script import Manager
from my_hoard.urls import app

manager = Manager(app)

if __name__ == "__main__":
    manager.run()