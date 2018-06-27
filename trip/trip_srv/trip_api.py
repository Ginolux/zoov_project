import socket
import threading
from uuid import uuid4
from flask import Blueprint, jsonify
# import pika
from flask_mongoengine import mongoengine
from flask_restful import Api, Resource
from kombu import Connection, Consumer, Exchange, Queue
import logging
import datetime

from .models import Bike_test, Trip_srv, Trip_test

trip_app = Blueprint('trip_app', __name__)
api = Api(trip_app)


class AllTrips(Resource):

    def get(self):
        # bikes = Bikes.objects.filter(id="bb3398hl52n3nnikktn0")
        # bikes = Bikes.objects.all().values_list('id')
        trip = Trip_test.objects.all()

        return jsonify({'all_trips': trip})

api.add_resource(AllTrips, '/')

# logging.basicConfig(level=logging.DEBUG)
class StartTrip(Resource):

    def get(self, bike_id):
        bike = Bike_test.objects.get(id=bike_id)

        
        if bike.status == 1:
            new_trip = Trip_test( 
                    bike_id=str(bike.id),
                    locations=[bike.location],
                    ended_at=""
                    )

            logging.debug('********Update bike id')
            bike.update(status=0) 
            bike.save()

            logging.debug('********Update trip id to 1')
            new_trip.status = 0

            logging.info('**********Start trip')
            new_trip.started_at = str(datetime.datetime.today())

            logging.debug('Create new record')
            ### trip.update(status=trip.status, started_at=trip.started_at, bike_id=trip.bike_id)
            new_trip.save()

            retrieve_new_trip = Trip_test.objects.get(id=new_trip.id) #Query database
            new_trip_id = str(retrieve_new_trip.id)

            logging.info('*******Return Trip ID')
            # return jsonify({'trip': trip.id})
            return jsonify({'New trip ID': new_trip_id})

            
        if not bike:
            return {'message': 'Bike not found.'}
            
api.add_resource(StartTrip, '/start/<string:bike_id>')


class EndTrip(Resource):
    def get(self, trip_id):
        trip = Trip_test.objects.get(id=trip_id)
        bike = Bike_test.objects.get(id=trip.bike_id)

        if bike.status == 0:
            logging.debug('********Update bike id')
            # bike = Bike_test.objects.get(id=trip.bike_id)
            bike.update(status=1) 
            bike.save()

            logging.debug('********Update trip id to 0: make available')
            trip.status = 1

            logging.info('*******End trip')
            trip.ended_at = str(datetime.datetime.today())

            logging.debug('Update database')
            trip.update(status=trip.status, ended_at=trip.ended_at)
            trip.save()

            return_trip = Trip_test.objects.get(id=trip_id)#Query database

            logging.info('*******Return Trip info to user')

            return jsonify({'trip': return_trip})

        return jsonify({'message': 'No new trip started with this id. Start new trip first.'})

api.add_resource(EndTrip, '/end/<string:trip_id>')







rabbit_url = "amqp://localhost:5672/"
conn = Connection(rabbit_url, heartbeat=10)
exchange = Exchange("example-exchange", type="direct")
queue = Queue(name="example-queue", exchange=exchange, routing_key="BOB")

def process_message(body, message):
    trip = Trip_test( 
                status=body['status'],
                bike_id=body['bike_id'],
                started_at=body['started_at'],
                ended_at=body['ended_at'],
                locations=body['locations']
                )

    # id = body['id']
    # if Trip_test.objects.with_id(id):
    #     trip.update()
    #     trip.save()


    # trip = Trip_test( 
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
