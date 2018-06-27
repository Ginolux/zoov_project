from mongoengine import Document, fields
# from bike.application import db

class Bike_test(Document):
    status = fields.IntField(required=True)
    location = fields.DictField(
        type = fields.StringField(required=True),
        coordinates = fields.ListField(required=True)
    )

class Trip_srv(Document):
    # _id = fields.ObjectIdField()
    # id = fields.StringField()
    bike_id = fields.StringField()
    status = fields.IntField(required=True)
    locations = fields.ListField(
        fields.DictField(
            type = fields.StringField(required=True),
            coordinates = fields.ListField(required=True)
        )
    )
    started_at = fields.StringField(required=True)
    ended_at = fields.StringField(required=True)



class Trip_test(Document):
    # _id = fields.ObjectIdField()
    # id = fields.StringField()
    bike_id = fields.StringField()
    status = fields.IntField(required=True)
    locations = fields.ListField(
        fields.DictField(
            type = fields.StringField(required=True),
            coordinates = fields.ListField(required=True)
        )
    )
    started_at = fields.StringField(required=True)
    ended_at = fields.StringField(required=True)


    
