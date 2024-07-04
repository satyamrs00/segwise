from flask import Blueprint, request, jsonify
from app.db import upload_file
from flask_cors import CORS
from datetime import datetime

from datetime import datetime, timedelta
from flask import current_app, request, jsonify, g

# import jwt

query_v1 = Blueprint(
    'query_v1', 'query_v1', url_prefix='/api')

CORS(query_v1)

@query_v1.route('upload_file', methods=["POST"])
def api_post_upload_file():
    """
    Upload a file.
    """
    
    file = request.files['file']
    
    if not file:
        return jsonify({"error": "No file provided"})
    
    try:
        upload_file(file)
        return jsonify({"message": "File uploaded successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
