import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
import bcrypt
import sys
import logging



app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'coffee_coastalview'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb+srv://JOS:Malteasers1!@cluster0.qn0az.mongodb.net/coffee_coastalview?retryWrites=true&w=majority')

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_cafes', methods=['GET'])
def get_cafes():
    if request.method == 'GET':
        return render_template("cafes.html",
                                cafes=mongo.db.cafes.find())


@app.route('/index', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

        if 'username' in session:
            return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
    handler = logging.FileHandler('test.log') # creates handler for the log file
    logger.addHandler(handler) # adds handler to the werkzeug WSGI logger
 
    if login_user:
        logger.info('Processing 88888888888888888 default request')
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('get_cafes'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

