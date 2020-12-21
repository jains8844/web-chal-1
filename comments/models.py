from flask_sqlalchemy import SQLAlchemy
from . import database as db

class Comment(db.Model):
    __tablename__ = 'comments'
    cid = db.Column(db.String, primary_key = True)
    comment = db.Column(db.String)
    password = db.Column(db.String)