from mongoengine import Document, fields
# from bike.application import db


class Bikes(Document):
    status = fields.IntField()
    location = fields.DictField(
        type = fields.StringField(required=True),
        coordinates = fields.ListField(required=True)
    )


class Bike_db(Document):
    status = fields.IntField(required=True)
    location = fields.DictField(
        type = fields.StringField(required=True),
        coordinates = fields.ListField(required=True)
    )


