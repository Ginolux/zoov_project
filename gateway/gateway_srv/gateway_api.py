import requests
from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from .models import Bike_db, Trip_db
from .gateway_publisher import EventsPublisher


gateway_app = Blueprint('gateway_app', __name__)
api = Api(gateway_app)


class BikesEndpoint(Resource):
    '''
    Bikes service
    '''
    def get(self):
        r = requests.get('http://0.0.0.0:8081')
        return r.json()

api.add_resource(BikesEndpoint, '/bikeservice')


class TripsEndpoint(Resource):
    '''
    Trips service
    '''
    def get(self):
        r = requests.get('http://0.0.0.0:8082')
        return r.json()

api.add_resource(TripsEndpoint, '/tripservice')




class BikeIdEndpoint(Resource):
    '''
    Get bike by id
    '''
    def get(self, bike_id):
        r = requests.get('http://0.0.0.0:8081/{}'.format(bike_id))
        return r.json()

api.add_resource(BikeIdEndpoint, '/bikeservice/<string:bike_id>')


class TripIdEndpoint(Resource):
    '''
    Get trip by id
    '''
    def get(self, trip_id):
        r = requests.get('http://0.0.0.0:8082/{}'.format(trip_id))
        return r.json()

api.add_resource(TripIdEndpoint, '/tripservice/<string:trip_id>')



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


class GatewayRoot(Resource):
    '''
    Gateway root
    '''
    def __init__(self):
        self.bikes_endpoint = BikesEndpoint()
        self.bike_id_endpoint = BikeIdEndpoint()
        self.trips_endpoint = TripsEndpoint()
        self.trip_id_endpoint = TripIdEndpoint()

    def get(self):
        allbikes = BikesEndpoint()
        return allbikes.get()

api.add_resource(GatewayRoot, '/')



class GatewayRouting(Resource):
    '''
    Gateway Iterface pattern
    '''

    def get(self, given_id):
        if Bike_db.objects.filter(id=given_id):
            data = Bike_db.objects.get(id=given_id)

            if data.status == 1:
                r = requests.get('http://0.0.0.0:8082/start/{}'.format(given_id))
                return r.json()

            elif data.status == 0:
                r = requests.get('http://0.0.0.0:8081/{}'.format(given_id))
                return r.json()

        r = requests.get('http://0.0.0.0:8082/end/{}'.format(given_id))
        return r.json()

api.add_resource(GatewayRouting, '/<string:given_id>')



class GatewayPublishEvent(Resource):
    '''
    Publish events received
    '''
    def post(self, event):
        publisher = EventsPublisher() # Call EventsPublisher class
        publisher.publish(event)

        return {'message': 'Event published'}

api.add_resource(GatewayPublishEvent, '/sendevent/<string:event>')

