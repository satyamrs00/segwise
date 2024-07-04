import os

from flask import Flask, jsonify
# from json import JSONEncoder
from flask_cors import CORS

# from bson import json_util, ObjectId
# from datetime import datetime, timedelta

# from app.api.auth import auth_v1
from app.api.query import query_v1


def create_app():

    APP_DIR = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)
    CORS(app)
    # app.json_encoder = MongoJsonEncoder
  
    # app.register_blueprint(auth_v1)
    app.register_blueprint(query_v1)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return jsonify({'error': 'Not found'}), 404

    return app