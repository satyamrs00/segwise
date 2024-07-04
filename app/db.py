from datetime import datetime
import os
import csv
from sqlalchemy import create_engine

from flask import g

from werkzeug.local import LocalProxy

from app.models import Game, SupportedLanguages, Categories, Genres, Tags, Base

from sqlalchemy.orm import Session
from sqlalchemy import select


def get_engine():
    if 'engine' not in g:
        g.engine = create_engine('sqlite:///games.db', echo=True)
        Base.metadata.create_all(g.engine)

    return g.engine


engine = LocalProxy(get_engine)


def get_datetime_from_string(dateString):
    """
    Convert date string to datetime.
    """
    return datetime.strptime(dateString, '%b %d, %Y') if len(dateString) > 8 else datetime.strptime(dateString, '%b %Y')


integerFields = ['appid', 'required_age', 'price', 'dlc_count', 'positive', 'negative', 'score_rank']
booleanFields = ['windows', 'mac', 'linux']
m2mFields = ['supported_languages', 'categories', 'genres', 'tags']
stringFields = ['name', 'about_the_game', 'developers', 'publishers']
dateFields = ['release_date']
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


def upload_file(file):
    """
    Upload a file.
    """
    try:
        with open (f"./uploads/{file.filename}", 'wb') as f:
            f.write(file.read())

        
        with Session(engine) as session:
                
            with open (f"./uploads/{file.filename}", encoding='utf-8', errors='ignore') as f:
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

                            if columns[i] in stringFields:
                                data[i] = data[i].strip()

                            if columns[i] in dateFields:
                                data[i] = get_datetime_from_string(data[i])

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
        os.remove(f"./uploads/{file.filename}")

    except Exception as e:
        print(e)
        raise e


def get_games(params):
    """
    Get all games.
    """
    try:
        with Session(engine) as session:

            stmt = select(Game)

            queryParams = {}            
            for key, value in params.items():
                if key in integerFields:
                    queryParams[key] = float(value) if key == 'price' else int(value)
                elif key in booleanFields:
                    queryParams[key] = True if value == 'True' else False
                elif key in stringFields:
                    queryParams[key] = value
                elif key in dateFields:
                    queryParams[key] = value
                elif key in m2mFields:
                    queryParams[key] = value.split(',')

            for key in queryParams:
                if key in integerFields or key in booleanFields:
                    stmt = stmt.where(getattr(Game, key) == queryParams[key])
                elif key in stringFields:
                    stmt = stmt.where(getattr(Game, key).like(f'%{queryParams[key]}%'))
                elif key in dateFields:
                    stmt = stmt.where(getattr(Game, key) == get_datetime_from_string(queryParams[key]))
                elif key in m2mFields:
                    for obj in queryParams[key]:
                        stmt = stmt.where(getattr(Game, key).any(getattr(mapColumnNameToModel[key], mapColumnNameToSingular[key]) == obj))

            games = session.execute(stmt).scalars().all()

            results = []
            for row in games:
                dictret = row.__dict__

                gId = dictret['id']
                for key in m2mFields:
                    vals = getattr(session.query(Game).where(Game.id == gId).one(), key)
                    dictret[key] = [val.__dict__[mapColumnNameToSingular[key]] for val in vals]

                dictret.pop('_sa_instance_state', None)
                dictret.pop('id', None)

                results.append(dictret)

            return results
            
    except Exception as e:
        print(e)
        raise e
