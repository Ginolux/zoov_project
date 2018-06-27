# import jsonify
from mongoengine import Document, connect, fields

connect(db= 'zoov',
                    host= 'localhost',
                    port= 27017,
                    username= 'test',
                    password= 'test'
    )


class Bike_test(Document):
    _id = fields.ObjectIdField()
    myid = fields.StringField(unique=True)
    status = fields.IntField(required=True)
    location = fields.DictField(
        type = fields.StringField(required=True),
        coordinates = fields.ListField(required=True)
    )

data = Bike_test.objects.first()

# for bike in data.
print(data.myid)
print(data.location)
print(data.status)


