from flask import Blueprint, request, jsonify
from app.db import login_user, add_user, token_required, update_emergency_contact
from flask_cors import CORS
from datetime import datetime

from datetime import datetime, timedelta
from flask import current_app, request, jsonify

import jwt

auth_v1 = Blueprint(
    'auth_v1', 'auth_v1', url_prefix='/auth')

CORS(auth_v1)


@auth_v1.route('/login', methods=["POST"])
def api_post_login():
    """
    Login a user.
    """
    post_data = request.get_json()
    try:
        email = post_data.get('email')
        password = post_data.get('password')

        if email is None or password is None:
            raise ValueError("email and password are required")
        
        login_result = login_user(email, password)

        if login_result is None:
            raise ValueError("login failed")
        
        jwt_token = jwt.encode({'email': email, 'exp': datetime.now() + timedelta(minutes=30)}, current_app.config['JWT_SECRET_KEY'])
        userObj = {a : login_result[a] for a in login_result if a != 'password' and a != '_id'}
        return jsonify({
            'token': jwt_token,
            'user': userObj
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@auth_v1.route('/register', methods=["POST"])
def api_post_register():
    """
    Register a user.
    """
    post_data = request.get_json()
    try:
        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')
        isMentor = post_data.get('isMentor')

        result = add_user(username, email, password, isMentor)
        
        if "error" in result:
            raise ValueError(result['error'])
    
        print(result)
        
        jwt_token = jwt.encode({'email': email, 'exp': datetime.now() + timedelta(minutes=30)}, current_app.config['JWT_SECRET_KEY'])
        userObj = {a : result["user"][a] for a in result["user"] if a != 'password' and a != '_id'}

        return jsonify({
            'token': jwt_token,
            'user': userObj
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@auth_v1.route('/user', methods=["GET"])
@token_required
def api_get_user(user):
    """
    Get user details.
    """
    try:
        userObj = {a : user[a] for a in user if a != 'password' and a != '_id'}
        return jsonify(userObj), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@auth_v1.route('/emergency_contact', methods=["POST"])
@token_required
def api_post_emergency_contact(user):
    """
    Add emergency contact.
    """
    post_data = request.get_json()
    try:
        emergency_contact = post_data.get('emergency_contact_number')
        relation_with_emergency_contact = post_data.get('emergency_relation')
        emergency_email = post_data.get('emergency_contact_email')
        user_id = user['userID']

        result = update_emergency_contact(user_id, emergency_contact, emergency_email, relation_with_emergency_contact)
        
        if "error" in result:
            raise ValueError(result['error'])
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400