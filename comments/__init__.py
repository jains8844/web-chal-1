from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

database = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getcwd()+'/database.db'
    database.init_app(app)

    with app.app_context():
        database.create_all()
        return app