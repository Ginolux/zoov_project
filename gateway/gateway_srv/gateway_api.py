import requests
from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from .models import Bikes


gateway_app = Blueprint('gateway_app', __name__)
api = Api(gateway_app)


class BikesEndpoint(Resource):
    '''
    Bikes service
    '''
    def get(self):
        r = requests.get('http://<ip_address>:8081/')
        return r.json()

api.add_resource(BikesEndpoint, '/bikeservice')


class TripsEndpoint(Resource):
    '''
    Trips service
    '''
    def get(self):
        r = requests.get('http://<ip_address>:8082/')
        return r.json()

api.add_resource(TripsEndpoint, '/tripservice')




class BikeIdEndpoint(Resource):
    '''
    Get bike by id
    '''
    def get(self, bike_id):
        r = requests.get('http://<ip_address>:8081/{}'.format(bike_id))
        return r.json()

api.add_resource(BikeIdEndpoint, '/bikeservice/<string:bike_id>')


class TripIdEndpoint(Resource):
    '''
    Get trip by id
    '''
    def get(self, trip_id):
        r = requests.get('http://<ip_address>:8082/{}'.format(trip_id))
        return r.json()

api.add_resource(TripIdEndpoint, '/bikeservice/<string:trip_id>')



class GatewayResources(Resource):
    '''
    Gateway Resources 
    '''
    def get(self):
        result = {
            'bike resource': 'http://<ip_address>:8081',
            'trip resource': 'http://<ip_address>:8082'
        }
        return {'Resources': result}

api.add_resource(GatewayResources, '/resources')


class Gateway(Resource):
    '''
    Gateway Iterface pattern
    '''
    def __init__(self):
        self.bikes_endpoint = BikesEndpoint()
        self.bike_id_endpoint = BikeIdEndpoint()
        self.trips_endpoint = TripsEndpoint()
        self.trip_id_endpoint = TripIdEndpoint()

    def get(self):
        result = {
            'bike resource': 'http://<ip_address>:8081',
            'trip resource': 'http://<ip_address>:8082'
        }
        return {'Resources': result}

api.add_resource(Gateway, '/')
