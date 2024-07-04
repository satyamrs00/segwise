import os

from flask import Flask, jsonify
from flask_cors import CORS

from app.api.query import query_v1


def create_app():

    APP_DIR = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(query_v1)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return jsonify({'error': 'Not found'}), 404

    return app