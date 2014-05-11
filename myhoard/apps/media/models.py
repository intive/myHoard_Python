import logging
from datetime import datetime
from PIL import Image, ImageOps

from werkzeug.exceptions import Forbidden, InternalServerError, NotFound

from flask import current_app, g
from flask.ext.mongoengine import Document
from mongoengine import MapField, ImageField, DateTimeField, ObjectIdField, ValidationError
from mongoengine.python_support import StringIO

logger = logging.getLogger(__name__)


class Media(Document):
    images = MapField(ImageField())
    created_date = DateTimeField(default=datetime.now)
    item = ObjectIdField()
    collection = ObjectIdField()
    owner = ObjectIdField()

    @property
    def public(self):
        from myhoard.apps.collections.models import Collection

        return bool(Collection.objects(id=self.collection, public=True).count()) if self.collection else True

    def __str__(self):
        return '<{} {}>'.format(type(self).__name__, self.id)

    @classmethod
    def get_visible_or_404(cls, media_id):
        from myhoard.apps.collections.models import Collection

        media = cls.objects.get_or_404(id=media_id)
        if media.collection:
            Collection.get_visible_or_404(media.collection)

        return media

    @classmethod
    def create(cls, image_file):
        if not image_file:
            raise ValidationError(errors={'image': 'Field is required'})

        media = cls()
        media.id = None
        media.created_date = None
        media.owner = g.user

        cls.create_image_files(media, image_file)

        logger.info('{} created'.format(media))
        return media.save()

    @classmethod
    def put(cls, media_id, image_file):
        media = cls.objects.get_or_404(id=media_id)
        if media.owner != g.user:
            raise Forbidden('Only collection owner can edit media') if media.public else NotFound()

        return cls.update(media, image_file)

    @classmethod
    def update(cls, media, image_file):
        if not image_file:
            raise ValidationError(errors={'image': 'Field is required'})

        for image in media.images.itervalues():
            image.delete()

        media.images = {}

        cls.create_image_files(media, image_file)

        media.save()
        logger.info('{} updated'.format(media))

        return media

    @classmethod
    def delete(cls, media_id):
        media = cls.objects.get_or_404(id=media_id)
        if media.owner != g.user:
            raise Forbidden('Only media owner can delete media') if media.public else NotFound()

        for image in media.images.itervalues():
            image.delete()

        super(cls, media).delete()
        logger.info('{} deleted'.format(media))

    @classmethod
    def create_from_item(cls, item):
        for media in cls.objects(id__in=item.media, item__not__exists=True, owner=g.user):
            media.item = item.id
            media.collection = item.collection

            media.save()
            logger.info('{} updated'.format(media))

        item.media = cls.objects(item=item.id).scalar('id')

        item.save()
        logger.info('{} media id\'s updated'.format(item))

    @classmethod
    def delete_from_item(cls, item):
        for media_id in cls.objects(item=item.id).scalar('id'):
            cls.delete(media_id)

    @classmethod
    def get_image_file(cls, media, size):
        if size:
            if (size in media.images) and (size != 'master'):
                image = media.images[size].get()
            else:
                raise ValidationError(errors={'size': 'Not in {}'.format(
                    ', '.join(str(size) for size in current_app.config['IMAGE_THUMBNAIL_SIZES']))})
        else:
            image = media.images['master'].get()

        return image

    @classmethod
    def open_image_file(cls, image_file):
        extensions = current_app.config['IMAGE_EXTENSIONS']
        if not ('.' in image_file.filename and image_file.filename.rsplit('.', 1)[1] in extensions):
            raise ValidationError(errors={'image': 'File extension is not {}'.format(', '.join(extensions))})

        try:
            image = Image.open(image_file)
            image_format = image.format
        except IOError:
            raise InternalServerError('No PIL drivers for that file type')

        return image, image_format

    @classmethod
    def create_image_files(cls, media, image_file):
        image, image_format = cls.open_image_file(image_file)

        for size in current_app.config['IMAGE_THUMBNAIL_SIZES']:
            cls.save_image_in_mapfield(
                ImageOps.fit(image, (size, size), Image.ANTIALIAS),
                image_format, media, str(size)
            )

        # since image is source stream for thumbnails
        # we are forced to save original image last
        cls.save_image_in_mapfield(image, image_format, media, 'master')

    # Super elastic workaround cost a little advanced usage
    # https://github.com/MongoEngine/mongoengine/issues/382
    # https://github.com/MongoEngine/mongoengine/pull/391
    @classmethod
    def save_image_in_mapfield(cls, image_obj, image_format, instance, index):
        io = StringIO()
        image_obj.save(io, image_format)
        io.seek(0)

        image_proxy = cls._fields['images'].field.get_proxy_obj('images', instance)
        image_proxy.put(io)

        instance.images[index] = image_proxy
