from mongoengine import Document, fields
# from bike.application import db


class Bike_srv(Document):
    # _id = fields.ObjectIdField()
    # id = fields.StringField()
    status = fields.IntField(required=True)
    location = fields.DictField(
        type = fields.StringField(required=True),
        coordinates = fields.ListField(required=True)
    )



class Bike_test(Document):
    status = fields.IntField(required=True)
    location = fields.DictField(
        type = fields.StringField(required=True),
        coordinates = fields.ListField(required=True)
    )


    
