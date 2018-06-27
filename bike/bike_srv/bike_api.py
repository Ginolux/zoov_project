import socket
import threading
from uuid import uuid4

from flask import Blueprint, jsonify
from flask_mongoengine import mongoengine
from flask_restful import Api, Resource
from kombu import Connection, Consumer, Exchange, Queue

from .models import Bike_db, Bikes

bike_app = Blueprint('bike_app', __name__)
api = Api(bike_app)


class AllBikes(Resource):

    def get(self):
        bikes = Bike_db.objects.all()

        return jsonify(bikes)

api.add_resource(AllBikes, '/')


class Bike(Resource):

    def get(self, bike_id):
        bike = Bike_db.objects.filter(id=bike_id)

        if not bike:
            return jsonify({'message': 'Bike not found'})

        return jsonify(bike)

api.add_resource(Bike, '/<string:bike_id>')


# class BikeTestDB(Resource):

#     def get(self):
#         # bikes = Bikes.objects.filter(id="bb3398hl52n3nnikktn0")
#         # bikes = Bikes.objects.all().values_list('id')
#         bikes = Bike_test.objects.all()

#         return jsonify({'all_movies': bikes})

# api.add_resource(BikeTestDB, '/movie')



rabbit_url = "amqp://localhost:5672/"
conn = Connection(rabbit_url, heartbeat=10)
exchange = Exchange("example-exchange", type="direct")
queue = Queue(name="example-queue", exchange=exchange, routing_key="BOB")

def process_message(body, message):
    # bike = Bike_db( 
    #             status=body['status'],
    #             location=body['location'])

    # id = body['id']
    # if Bike_test.objects.with_id(id):
    #     bike.update()
    #     bike.save()


    # bike = Bike_test( 
    #                 status=body['status'],
    #                 location=body['location'])
    # bike.update()
    # bike.save()
    # bike.drop_collection()

    print("The body is {}".format(body))
    message.ack()

consumer = Consumer(conn, queues=queue, callbacks=[process_message], accept=["application/json"])
consumer.consume()

def establish_connection():
    revived_connection = conn.clone()
    revived_connection.ensure_connection(max_retries=3)
    channel = revived_connection.channel()
    consumer.revive(channel)
    consumer.consume()
    return revived_connection

def consume():
    new_conn = establish_connection()
    while True:
        try:
            new_conn.drain_events(timeout=2)
        except socket.timeout:
            new_conn.heartbeat_check()

def consumer_deamon():
    while True:
        try:
            consume()
        except conn.connection_errors:
            print("connection revived")

# consumer_deamon()
d = threading.Thread(name='daemon', target=consumer_deamon)
d.setDaemon(True)
d.start()
