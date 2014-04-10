from datetime import datetime
from PIL import Image, ImageOps

from flask import current_app, g
from flask.ext.mongoengine import Document
from mongoengine import MapField, ImageField, DateTimeField, \
    ObjectIdField, ValidationError
from mongoengine.python_support import StringIO


class Media(Document):
    images = MapField(ImageField())
    created_date = DateTimeField(default=datetime.now)
    item = ObjectIdField()
    owner = ObjectIdField()

    def __repr__(self):
        return '<Media {}>'.format(self.id)

    @classmethod
    def create(cls, image_file):
        def put_image(image_obj, index):
            io = StringIO()
            image_obj.save(io, image_format)
            io.seek(0)

            image_proxy = cls._fields['images'].field.get_proxy_obj('images',
                                                                    media)
            image_proxy.put(io)

            media.images[index] = image_proxy

        if not image_file:
            raise ValidationError(errors={'image': 'Field is required'})

        media = cls()
        media.id = None
        media.created_date = None
        media.owner = g.user

        try:
            image = Image.open(image_file)
            image_format = image.format
        except:
            raise ValidationError(errors={'image': 'Unsupported image type'})

        for size in current_app.config['IMAGE_THUMBNAIL_SIZES']:
            put_image(ImageOps.fit(image, (size, size), Image.ANTIALIAS),
                      str(size))

        put_image(image, 'master')

        return media.save()

    @classmethod
    def update(cls, media_id, image_file):
        medium = cls.objects.get_or_404(id=media_id, owner=g.user)

        if not image_file:
            raise ValidationError(errors={'image': 'Field is required'})

        image = image_file

        medium.image.delete()
        medium.image = image
        medium.save()

    @classmethod
    def delete_(cls, media_id):
        pass

    @classmethod
    def create_from_item(cls, item):
        for media in Media.objects(id__in=item.media, item__not__exists=True,
                                   owner=g.user):
            media.item = item.id
            media.save()

        item.media = list(Media.objects(item=item.id))
        item.save()

    @classmethod
    def update_from_item(cls, item, update_item):
        pass

    @classmethod
    def delete_from_item(cls, item):
        pass