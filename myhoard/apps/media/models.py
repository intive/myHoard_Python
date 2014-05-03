from datetime import datetime
from PIL import Image, ImageOps
import logging

from flask import current_app, g
from flask.ext.mongoengine import Document
from mongoengine import MapField, ImageField, DateTimeField, \
    ObjectIdField, ValidationError
from mongoengine.python_support import StringIO

logger = logging.getLogger(__name__)


class Media(Document):
    images = MapField(ImageField())
    created_date = DateTimeField(default=datetime.now)
    item = ObjectIdField()
    owner = ObjectIdField()

    def __repr__(self):
        return '<Media {}>'.format(self.id)

    @classmethod
    def create(cls, image_file):
        if not image_file:
            raise ValidationError(errors={'image': 'Field is required'})

        media = cls()
        media.id = None
        media.created_date = None
        media.owner = g.user

        try:
            image = Image.open(image_file)
            image_format = image.format
        except IOError:
            raise ValidationError(
                errors={'image': 'No PIL drivers for that file type'})

        for size in current_app.config['IMAGE_THUMBNAIL_SIZES']:
            cls.save_image_in_mapfield(
                ImageOps.fit(image, (size, size), Image.ANTIALIAS),
                image_format, media, str(size))

        # since image is source stream for thumbnails
        # we are forced to save original image last
        cls.save_image_in_mapfield(image, image_format, media, 'master')

        return media.save()

    @classmethod
    def put(cls, media_id, image_file):
        media = cls.objects.get_or_404(id=media_id, owner=g.user)

        return cls.update(media, image_file)

    @classmethod
    def update(cls, media, image_file):
        if not image_file:
            raise ValidationError(errors={'image': 'Field is required'})

        # TODO: Fix this
        media.image.delete()
        media.image = image_file

        media.save()
        # TODO: Cascade update here

        return media

    @classmethod
    def delete(cls, media_id):
        media = Media.objects.get_or_404(id=media_id)
        # TODO: Fix this
        media.image.delete()

        return super(cls, media).delete()

    # Super elastic workaround cost a little advanced usage
    # https://github.com/MongoEngine/mongoengine/issues/382
    # https://github.com/MongoEngine/mongoengine/pull/391
    @classmethod
    def save_image_in_mapfield(cls, image_obj, image_format, instance, index):
        io = StringIO()
        image_obj.save(io, image_format)
        io.seek(0)

        image_proxy = cls._fields['images'].field.get_proxy_obj('images',
                                                                instance)
        image_proxy.put(io)

        instance.images[index] = image_proxy

    @classmethod
    def create_from_item(cls, item):
        for media in cls.objects(id__in=item.media, item__not__exists=True,
                                 owner=g.user):
            media.item = item.id
            media.save()

        item.media = cls.objects(item=item.id).scalar('id')

        item.save()

    @classmethod
    def update_from_item(cls, item, update_item):
        pass

    @classmethod
    def delete_from_item(cls, item):
        pass