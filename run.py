from app.factory import create_app

import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    app.config['DB_URI'] = config['TEST']['DB_URI']
    app.config['UPLOAD_FOLDER'] = './uploads/'
    # app.config['JWT_SECRET_KEY'] = config['PROD']['JWT_SECRET_KEY']
    # app.config['AWS_ACCESS_KEY'] = config['PROD']['AWS_ACCESS_KEY']
    # app.config['AWS_SECRET_ACCESS_KEY'] = config['PROD']['AWS_SECRET_ACCESS_KEY']

    with app.app_context():
        app.run()