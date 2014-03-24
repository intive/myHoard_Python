from flask import current_app


def check_image_file(file):
    # TODO Move validation to validate method in Menium class (raise ValidationError instead of FileError);
    # TODO in view fill Medium fields, call validate and if no errors were found call save method
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1] in
        current_app.config['IMAGE_EXTENSIONS']):
        raise FileError(
            'ERROR_CODE_MEDIA_BAD_EXT',
            errors={
                'image': 'File extension is not {}'.format(
                    ', '.join(current_app.config['IMAGE_EXTENSIONS']))
            }
        )