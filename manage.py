from flask.ext.script import Manager
from my_hoard import app

manager = Manager(app)

if __name__ == "__main__":
    manager.run()