from flask import Response
from flask.ext.restful import Resource, marshal_with, fields, request

from myhoard.apps.auth.decorators import login_required

from models import Media

media_fields = {
    'id': fields.String,
}


class MediaDetails(Resource):
    method_decorators = [login_required]

    @staticmethod
    def get(media_id):
        media = Media.get_visible_or_404(media_id)
        image = Media.get_image_file(media, request.args.get('size'))

        return Response(image, mimetype='image/' + image.format, direct_passthrough=True)

    @staticmethod
    @marshal_with(media_fields)
    def put(media_id):
        return Media.put(media_id, request.files.get('image'))

    @staticmethod
    def delete(media_id):
        Media.delete(media_id)

        return '', 204


class MediaList(Resource):
    method_decorators = [marshal_with(media_fields), login_required]

    @staticmethod
    def post():
        return Media.create(request.files.get('image')), 201