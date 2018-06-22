from flask import Flask
from flask_mongoengine import MongoEngine
from gateway_srv.gateway_api import gateway_app

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    app.register_blueprint(gateway_app)

    db.init_app(app)

    return app

