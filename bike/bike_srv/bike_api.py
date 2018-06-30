import logging
import threading
from uuid import uuid4

from flask import Blueprint, jsonify
from flask_mongoengine import mongoengine
from flask_restful import Api, Resource

from .bike_consumer import EventsConsumer
from .models import Bike_db, Bikes



bike_app = Blueprint('bike_app', __name__)
api = Api(bike_app)


class AllBikes(Resource):
    '''
    Return all the bikes
    '''
    def get(self):
        bikes = Bike_db.objects.all()

        return jsonify(bikes)

api.add_resource(AllBikes, '/')


class Bike(Resource):
    '''
    Return bike corresponding to the ID
    '''
    def get(self, bike_id):
        bike = Bike_db.objects.filter(id=bike_id)

        if not bike:
            return jsonify({'message': 'Bike not found'})

        return jsonify(bike)

api.add_resource(Bike, '/<string:bike_id>')



'''
Consumer deamon 
'''
logging.basicConfig(level=logging.DEBUG)

listen = EventsConsumer()
d = threading.Thread(name='daemon', target=listen.consumer_deamon)
d.setDaemon(True)
d.start()
