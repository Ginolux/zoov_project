from mongoengine import Document, fields
from application import db


class Bikes(db.Document):
    _id = fields.ObjectIdField()
    id = fields.StringField()
    location = fields.DictField(
        btype = fields.StringField(required=True),
        coordinates = fields.ListField(required=True)
    )
    

    meta = {}

