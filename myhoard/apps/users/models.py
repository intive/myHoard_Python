from mongoengine import Document, StringField, EmailField

class User(Document):
	username = StringField(unique=True, required=True)
	email = EmailField(unique=True, required=True)
	password = StringField(required=True)

	meta = {
		'indexes': ['username'],
	}