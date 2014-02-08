from flask.ext.restful import Api, Resource


class Collections(Resource):
    def __init__(self):
        super(Collections, self).__init__()

    def post(self):
        pass

    def get(self):
        pass

    def put(self):
        pass

    def delete(self, slug):
        pass


def demo():
    return "demo"