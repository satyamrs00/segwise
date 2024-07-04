# import bcrypt

import os
import csv
import sqlitecloud
from sqlalchemy import create_engine

# from datetime import datetime, timedelta
from flask import current_app, request, jsonify, g

from werkzeug.local import LocalProxy
# from flask_pymongo import PyMongo
# from functools import wraps
# import jwt

from app.models import Game, SupportedLanguages, Categories, Genres, Tags, Base

from sqlalchemy.orm import Session
from sqlalchemy import select



def get_engine():
    if 'engine' not in g:
        g.engine = create_engine('sqlite:///games.db', echo=True)
        Base.metadata.create_all(g.engine)

    return g.engine


engine = LocalProxy(get_engine)


def upload_file(file):
    """
    Upload a file.
    """
    try:
        with open (os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename), 'wb') as f:
            f.write(file.read())

        integerFields = ['appid', 'required_age', 'price', 'dlc_count', 'positive', 'negative', 'score_rank']
        booleanFields = ['windows', 'mac', 'linux']
        m2mFields = ['supported_languages', 'categories', 'genres', 'tags']
        mapColumnNameToModel = {
            'supported_languages': SupportedLanguages,
            'categories': Categories,
            'genres': Genres,
            'tags': Tags
        }
        mapColumnNameToSingular = {
            'supported_languages': 'supported_language',
            'categories': 'category',
            'genres': 'genre',
            'tags': 'tag'
        }
        
        with Session(engine) as session:
                
            # save the file to the static folder
            with open (os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename), encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                columns = next(reader) 
                
                for i in range(len(columns)):
                    columns[i] = columns[i].replace(' ', '_').lower()

                for data in reader:
                    map = {}
                    for i in range(len(data)):
                        if columns[i] and columns[i] not in m2mFields:
                            if columns[i] in integerFields:
                                if (data[i] == ''):
                                    data[i] = 0
                                data[i] = float(data[i]) if columns[i] == 'price' else int(data[i])

                            if columns[i] in booleanFields:
                                data[i] = True if data[i] == 'TRUE' else False
                                
                            map[columns[i]] = data[i]

                        elif columns[i] in m2mFields:
                            if not data[i]:
                                continue

                            if columns[i] == 'supported_languages':
                                data[i] = data[i][1:-1]

                            objects = []
                            for individualData in data[i].split(','):
                                individualData = individualData.strip()

                                if columns[i] == 'supported_languages':
                                    individualData = individualData[1:-1]
                                
                                obj = session.query(mapColumnNameToModel[columns[i]]).filter(getattr(mapColumnNameToModel[columns[i]], mapColumnNameToSingular[columns[i]]) == individualData).first()
                                if not obj:
                                    obj = mapColumnNameToModel[columns[i]](**{mapColumnNameToSingular[columns[i]]: individualData})
                                    session.add(obj)
                                    session.commit()
                                objects.append(obj)
                            map[columns[i]] = objects

                    game = Game(**map)
                    session.add(game)
                    session.commit()
                    
        # delete the file
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))

    except Exception as e:
        print(e)
        raise e


# decorator for verifying the JWT
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         # jwt is passed in the request header
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
        
#         # return 401 if token is not passed
#         if not token:
#             return jsonify({'message' : 'Token is missing !!'}), 401
  
#         try:
#             # decoding the payload to fetch the stored details
#             data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
#             current_user = db.users.find_one({"email": data['email']})
#         except Exception as e:
#             print(e)
#             return jsonify({
#                 'message' : 'Token is invalid !!'
#             }), 401
#         # returns the current logged in users context to the routes
#         return  f(current_user, *args, **kwargs)
  
#     return decorated
  

# def login_user(email, password):
#     """
#     Login a user with email and password
#     """
#     user = db.users.find_one({"email": email})

#     if user:
#         userBytes = password.encode('utf-8') 
#         result = bcrypt.checkpw(userBytes, user.get('password'))
#         if result:
#             return user
#         else:
#             return None
#     else:
#         return None

    
# def add_user(username, email, password, isMentor):
#     """
#     Add a user with email and password
#     """
#     try:
#         userbyemail = db.users.find_one({"email": email})
#         userbyusername = db.users.find_one({"username": username})
        
#         if userbyemail:
#             return {"error": "User already exists with this email"}
#         elif userbyusername:
#             return {"error": "User already exists with this username"}
#         else: 
#             bytes = password.encode('utf-8') 
#             salt = bcrypt.gensalt() 
#             hash = bcrypt.hashpw(bytes, salt) 

#             db.users.insert_one({
#                 "userID": str(ObjectId()),
#                 "username": username,
#                 "email": email,
#                 "password": hash,
#             })
#             return {
#                 "message": "User added successfully",
#                 # "user": {a: b for a, b in db.users.find_one({"email": email}).items() if a != "_id" and a != "password"}
#             }
            
#     except Exception as e:
#         return {"error": str(e)}
    
