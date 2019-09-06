from mongoengine import Document
from mongoengine.fields import (
    StringField,
    EmailField,
    IntField,
    ListField,
    EmbeddedDocumentField,
    FloatField
)
from .run import Run


class User(Document):
    meta = {'collection': 'user'}
    first_name = StringField()
    last_name = StringField()
    age = IntField()
    mass = FloatField()
    email = EmailField()
    runs = ListField(EmbeddedDocumentField(Run))