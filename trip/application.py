from flask import Flask
from flask_mongoengine import MongoEngine

from trip_srv.trip_api import trip_app

# from flask_restful import Resource, Api

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    app.register_blueprint(trip_app)

    db.init_app(app)

    return app
