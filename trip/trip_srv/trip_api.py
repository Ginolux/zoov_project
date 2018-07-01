import datetime
import logging
import threading
from uuid import uuid4

from flask import Blueprint, jsonify
from flask_mongoengine import mongoengine
from flask_restful import Api, Resource

from .models import Bike_db, Trip_db
from .trip_consumer import EventsConsumer


trip_app = Blueprint('trip_app', __name__)
api = Api(trip_app)


class AllTrips(Resource):
    '''
    Return all previous trips
    '''
    def get(self):
        trips = Trip_db.objects.all()

        return jsonify(trips)

api.add_resource(AllTrips, '/')


class Trip(Resource):
    '''
    Return a trip 
    '''
    def get(self, trip_id):
        trip = Trip_db.objects.filter(id=trip_id)

        return jsonify(trip)

api.add_resource(Trip, '/<string:trip_id>')


# logging.basicConfig(level=logging.DEBUG)
class StartTrip(Resource):
    '''
    Receive bike id and start a new trip
    '''
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
    '''
    End the new trip
    '''
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


'''
Consumer deamon 
'''
logging.basicConfig(level=logging.DEBUG)

listen = EventsConsumer()
d = threading.Thread(name='daemon', target=listen.consumer_deamon)
d.setDaemon(True)
d.start()
