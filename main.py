import dotenv
dotenv.load_dotenv('.env')

from comments.app import app
from comments import database as db
from comments.db import add_comment
from flask.sessions import SecureCookieSessionInterface
import os
import json
from comments.models import Comment


def init():
    adminsession = dict()
    adminsession['password'] = os.environ.get('ADMIN_PASS')
    session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)
    cookie = session_serializer.dumps(adminsession)
    os.environ['ADMIN_COOKIE'] = str(cookie)
    flag_cids = json.dumps([os.environ.get('FLAG_CID')])
    os.environ['ADMIN_CIDS'] = flag_cids
    with app.app_context():
        add_comment(os.environ.get('FLAG'), os.environ.get('ADMIN_PASS'), os.environ.get('FLAG_CID'))

init()

if(__name__ == '__main__'):
    app.run(port=8080)