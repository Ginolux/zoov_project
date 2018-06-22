from application import create_app
from flask_restful import Resource, Api
from flask import Blueprint
from flask import jsonify

from .models import Bikes
# import bikes_db

# bikes = bikes_db

gateway_app = Blueprint('gateway_app', __name__)
api = Api(gateway_app)

# class AllBikes(Resource):

#     def get(self, name):
#         return {'owner': name}

# api.add_resource(AllBikes, '/owner/<string:name>')

class AllBikes(Resource):

    def get(self):
        # bikes = Bikes.objects.filter(id="bb3398hl52n3nnikktn0")
        bikes = Bikes.objects.all().values_list('id')

        return jsonify({'all_bikes': bikes})

api.add_resource(AllBikes, '/')

class Bike(Resource):

    def get(self, bike_id):
        bike = Bikes.objects.filter(id=bike_id)

        return jsonify({'bike': bike})

api.add_resource(Bike, '/<string:bike_id>')