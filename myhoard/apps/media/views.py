from datetime import datetime

from flask import Response
from flask.ext.restful import Resource, marshal_with, fields, request

from myhoard.apps.common.errors import FileError
from myhoard.apps.common.decorators import custom_errors
from myhoard.apps.common.utils import get_request_json
from myhoard.apps.auth.decorators import login_required

from models import Medium

media_fields = {
    'id': fields.String,
}


class Media(Resource):
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

        args = get_request_json()
        for key, value in args.items():
            setattr(medium, key, value)

        medium.created_date = datetime.now()
        medium.save()

        return medium

    def delete(self, id):
        medium = Medium.objects.get(id=id)
        medium.delete()

        return '', 204


class MediaList(Resource):
    method_decorators = [marshal_with(media_fields), login_required,
                         custom_errors]

    def post(self):
        if 'image' not in request.files:
            raise FileError(
                'ERROR_CODE_NO_INCOMING_FILE_DATA',
                errors={'file': 'Field is required'}
            )

        medium = Medium(image=request.files['image'])
        medium.created_date = datetime.now()
        medium.save()

        return medium, 201