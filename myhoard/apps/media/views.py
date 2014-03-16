from datetime import datetime

from flask import Response
from flask.ext.restful import Resource, marshal_with, fields, request

from myhoard.apps.common.errors import FileError
from myhoard.apps.common.decorators import custom_errors
from myhoard.apps.auth.decorators import login_required

from models import Medium
from utils import check_image_file

media_fields = {
    'id': fields.String,
}


class MediaDetails(Resource):
    method_decorators = [custom_errors]

    def get(self, id):
        medium = Medium.objects.get(id=id)

        if request.url.endswith('thumbnail'):
            image = medium.image.thumbnail
        else:
            image = medium.image.get()

        return Response(image, mimetype='image/' + image.format,
                        direct_passthrough=True)

    @marshal_with(media_fields)
    def put(self, id):
        medium = Medium.objects.get(id=id)

        if 'image' not in request.files:
            raise FileError(
                'ERROR_CODE_NO_INCOMING_FILE_DATA',
                errors={'image': 'Field is required'}
            )

        image = request.files['image']
        check_image_file(image)

        medium.image.delete()
        medium.image = image
        medium.save()

        return medium

    def delete(self, id):
        medium = Medium.objects.get(id=id)
        medium.image.delete()
        medium.delete()

        return '', 204


class MediaList(Resource):
    method_decorators = [marshal_with(media_fields), login_required,
                         custom_errors]

    def post(self):
        if 'image' not in request.files:
            raise FileError(
                'ERROR_CODE_NO_INCOMING_FILE_DATA',
                errors={'image': 'Field is required'}
            )

        image = request.files['image']
        check_image_file(image)

        medium = Medium(image=image)
        medium.created_date = datetime.now()
        medium.save()

        return medium, 201