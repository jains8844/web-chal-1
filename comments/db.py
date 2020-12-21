import sqlite3
import uuid
from . import database as db
from .models import Comment

def add_comment(comment, password, cid=None):
    query = 'INSERT INTO comments(cid, comment, password) VALUES (?, ?, ?)'
    if(cid is None):
        cid = str(uuid.uuid4().hex)
    db.engine.execute(query, (cid, comment, password))
    return cid


def get_comments(cid, password):
    query = 'SELECT comment from comments WHERE cid="{}" AND password="{}"'.format(cid, password)
    result = db.engine.execute(query).fetchone()
    if(result is None or len(result)==0):
        return "Invaid Access", 403
    comment = result[0]
    return (comment, 200)
