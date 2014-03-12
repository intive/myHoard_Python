from flask import current_app

from myhoard.apps.common.errors import FileError


def check_image_file(file):
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1] in
        current_app.config['IMAGE_EXTENSIONS']):
        raise FileError(
            'ERROR_CODE_MEDIA_BAD_EXT',
            errors={
                'image': 'File extension is not {}'.format(
                    ', '.join(current_app.config['IMAGE_EXTENSIONS']))
            }
        )