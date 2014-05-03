from flask import abort, Response
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
        media = Media.objects.get_or_404(id=media_id)

        if 'size' in request.args:
            size = request.args['size']
            if size in media.images and (size != 'master'):
                image = media.images[request.args['size']].get()
            else:
                abort(404)
        else:
            image = media.images['master'].get()

        return Response(image, mimetype='image/' + image.format,
                        direct_passthrough=True)

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