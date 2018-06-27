import datetime
import logging
import socket
import threading
from uuid import uuid4

from flask import Blueprint, jsonify
from flask_mongoengine import mongoengine
from flask_restful import Api, Resource
from kombu import Connection, Consumer, Exchange, Queue

from .models import Bike_db, Trip_db

trip_app = Blueprint('trip_app', __name__)
api = Api(trip_app)


class AllTrips(Resource):

    def get(self):
        trips = Trip_db.objects.all()

        return jsonify(trips)

api.add_resource(AllTrips, '/')


class Trip(Resource):

    def get(self, trip_id):
        trip = Trip_db.objects.filter(id=trip_id)

        return jsonify(trip)

api.add_resource(Trip, '/<string:trip_id>')


# logging.basicConfig(level=logging.DEBUG)
class StartTrip(Resource):

    def get(self, bike_id):
        bike = Bike_db.objects.get(id=bike_id)

        
        # if bike.status == 1:  # recheck bike status
        new_trip = Trip_db( 
                bike_id=str(bike.id),
                locations=[bike.location],
                ended_at=""
                )

        # update bike status to 0 (ie. non available)
        bike.update(status=0) 
        bike.save()
        
        new_trip.status = 0       # set trip status to 0 (ie. non available)

        new_trip.started_at = str(datetime.datetime.today())      # record started time

        new_trip.save()     # create trip record

        retrieve_new_trip = Trip_db.objects.get(id=new_trip.id)   # query database to retrieve created trip
        new_trip_id = str(retrieve_new_trip.id)     # get new trip id

        return jsonify({'New trip ID': new_trip_id})

            
api.add_resource(StartTrip, '/start/<string:bike_id>')


class EndTrip(Resource):
    def get(self, trip_id):
        trip = Trip_db.objects.get(id=trip_id)
        bike = Bike_db.objects.get(id=trip.bike_id)

        if bike.status == 0: # recheck bike status
            logging.debug('********Update bike id')
            # bike = Bike_db.objects.get(id=trip.bike_id)
            bike.update(status=1)  # update bike status to 1 (ie. available)
            bike.save()

            trip.status = 1     # update trip status to 1 (ie. available)

            logging.info('*******End trip')
            trip.ended_at = str(datetime.datetime.today())      # record end time

            logging.debug('Update database')
            trip.update(status=trip.status, ended_at=trip.ended_at)     # update trip record
            trip.save()

            return_trip = Trip_db.objects.get(id=trip_id)     #query database

            return jsonify(return_trip)

        return jsonify({'message': 'No new trip started with this id. Start new trip first.'})

api.add_resource(EndTrip, '/end/<string:trip_id>')





rabbit_url = "amqp://localhost:5672/"
conn = Connection(rabbit_url, heartbeat=10)
exchange = Exchange("example-exchange", type="direct")
queue = Queue(name="example-queue", exchange=exchange, routing_key="BOB")

def process_message(body, message):
    trip = Trip_db( 
                status=body['status'],
                bike_id=body['bike_id'],
                started_at=body['started_at'],
                ended_at=body['ended_at'],
                locations=body['locations']
                )

    # id = body['id']
    # if Trip_db.objects.with_id(id):
    #     trip.update()
    #     trip.save()


    # trip = Trip_db( 
    #                 status=body['status'],
    #                 location=body['location'])
    # trip.update()
    trip.save()
    # trip.drop_collection()

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
