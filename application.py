from flask import Flask
from flask_mongoengine import MongoEngine
# from flask_restful import Resource, Api

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    from gateway.gateway import gateway_app
    app.register_blueprint(gateway_app)

    db.init_app(app)

    return app

