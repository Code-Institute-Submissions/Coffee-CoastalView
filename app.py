import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
import bcrypt


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'coffee_coastalview'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb+srv://JOS:Malteasers1!@cluster0.qn0az.mongodb.net/coffee_coastalview?retryWrites=true&w=majority')

mongo = PyMongo(app)

#loads cafe page with all cafes in Mongo
@app.route('/get_cafes')
def get_cafes():
        return render_template("cafes.html",
                                cafes=mongo.db.cafes.find())


@app.route('/get_profile')
def get_profile():
        return render_template("myprofile.html")                                


#loads login page
@app.route('/index', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

        if 'username' in session:
            return 'You are logged in as ' + session['username']

    return render_template('index.html')


#checks to see user login details exist/are correct and if correct returns user to cafes page
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return render_template('cafes.html',
                                    cafes=mongo.db.cafes.find())

    return 'Invalid username/password combination'


#brings user to registration page
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

