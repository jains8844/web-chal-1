from flask import Flask, render_template, request, session, redirect, make_response, flash, url_for
import os
import json
import uuid
from .visit import q, visit_url

from .db import get_comments, add_comment

from . import create_app

app = create_app()

@app.before_request
def func():
    if(session.get('password') is None):
        session['password'] = str(uuid.uuid4().hex)

def sqlicheck(string):
    string = str(string).replace(' ', '').replace('-', '').replace(';', '').replace('\'', '').replace('(', '').replace(')', '').replace(',', '')
    return string

@app.route('/comment', methods=['GET'])
def index():
    search_query = sqlicheck(request.args.get('cid'))
    if(session.get('password') is None):
        return "Invalid Access", 403
    comments = get_comments(search_query, sqlicheck(session['password']))
    return comments

@app.route('/', methods = ['GET', 'POST'])
@app.route('/add', methods=['GET', 'POST'])
def add():
    if(request.method == 'GET'):
        resp = make_response(render_template('index.html'))
        if(request.cookies.get('cids') is None):
            resp.set_cookie('cids', json.dumps([]))
        return resp
    comment = request.form['comment']
    uid = add_comment(comment, session['password'])
    resp = make_response(redirect('/comment?cid={}'.format(uid)))
    if(request.cookies.get('cids')):
        l = json.loads(request.cookies.get('cids'))
        l.append(uid)
        resp.set_cookie('cids', json.dumps(l))
    else:
        resp.set_cookie('cids', json.dumps([]))
    return resp

@app.route('/url', methods = ['POST'])
def visiturl():
    url = request.form.get('url')
    q.enqueue(visit_url, url, json.dumps(dict(os.environ)), result_ttl=600)
    flash('The admin will visit the url soon.')
    return redirect(url_for('add'))

if(__name__=="__main__"):
    app.run(port = 8080)
