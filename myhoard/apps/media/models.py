from flask import current_app
from mongoengine import Document, ImageField, DateTimeField, ObjectIdField


class Medium(Document):
    image = ImageField(thumbnail_size=current_app.config['IMAGE_THUMBNAIL'])
    created_date = DateTimeField()
    collection = ObjectIdField()
