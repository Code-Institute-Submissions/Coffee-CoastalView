import os
from flask import Flask, render_template, redirect, request, url_for, session, g
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


#loads each individual cafe page when see more button clicked
@app.route('/get_individualcafe/<cafe_id>')
def get_individualcafe(cafe_id):
        return render_template("individualcafe.html",
                                cafe=mongo.db.cafes.find_one({'_id': ObjectId(cafe_id)}),
                                review=mongo.db.reviews.find())


#loads user profile page if user logged in, if user not logged in loads log in page 
@app.route('/get_profile')
def get_profile():
        if session.get('USERNAME', None):
            username = session['USERNAME']
            return render_template("myprofile.html",
                                    cafes=mongo.db.cafes.find(), user_data=existing_user, 
                                    users_password=users_password)          
        
        # User not signed in
        return render_template('index.html')                                                      


#loads login page and takes user to profile page if login details correct
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('get_profile'))
    if request.method == 'GET':
        return render_template('index.html')

        if 'username' in session:
            return 'You are logged in as ' + session['username']

    return render_template("myprofile.html",
                            user=mongo.db.users.find())


#checks to see user login details exist/are correct and if correct returns user to cafes page
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return render_template('myprofile.html',
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
            return render_template('myprofile.html')
        
        return 'That username already exists!'

    return render_template('register.html')

#logs user out 
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template("cafes.html",
                                cafes=mongo.db.cafes.find())


#leaves user add review
@app.route('/add_review', methods=['POST'])
def add_review():
    reviews = mongo.db.reviews
    reviews.insert_one(request.form.to_dict())
    return redirect(url_for('get_profile'))


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

