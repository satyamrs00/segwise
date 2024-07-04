from flask import Blueprint, request, jsonify, g
from app.db import upload_file, get_games
from flask_cors import CORS


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
        raise e
    

@query_v1.route('query', methods=["GET"])
def api_get_query():
    """
    Query the database.
    """

    params = request.args

    try:
        games = get_games(params)
        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)})
    