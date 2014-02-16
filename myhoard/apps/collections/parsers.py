from wtforms import Form
from wtforms.fields import FieldList, StringField
from wtforms import validators
import wtforms_json

wtforms_json.init()


class CollectionForm(Form):
    name = StringField('name', [validators.required(), validators.Length(min=3, max=25)])
    description = StringField('description', [validators.required(), validators.Length(min=3, max=250)])
    tags = FieldList(StringField())