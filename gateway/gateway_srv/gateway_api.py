# import pika
# import uuid
import requests
from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from .models import Bikes

# import bikes_db

# bikes = bikes_db

gateway_app = Blueprint('gateway_app', __name__)
api = Api(gateway_app)

# Bike service
class BikesEndpoint(Resource):
    def get(self):
        r = requests.get('http://localhost:8081/')
        return r.json()

api.add_resource(BikesEndpoint, '/bikeservice')


# Send id to Bike service
class BikeIdEndpoint(Resource):
    def get(self, bike_id):
        r = requests.get('http://localhost:8081/{}'.format(bike_id))
        return r.json()

api.add_resource(BikeIdEndpoint, '/bikeservice/<string:bike_id>')


class Gateway(Resource):
    def __init__(self):
        self.bikes_endpoint = BikesEndpoint()
        self.bike_id_endpoint = BikeIdEndpoint()

    def get(self):
        result = {
            'bikes endpoint': self.bikes_endpoint.get(),
            'bike id endpoint': self.bike_id_endpoint.get('bb2cdchl52n4orsopmtg')
        }
        return result

api.add_resource(Gateway, '/')
