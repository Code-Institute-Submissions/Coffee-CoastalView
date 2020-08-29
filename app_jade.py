import os
from flask import Flask, render_template, redirect, request, url_for, session, g
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
import bcrypt


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'coffee_coastalview'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb+srv://JOS:Malteasers1!@cluster0.qn0az.mongodb.net/coffee_coastalview?retryWrites=true&w=majority')

mongo = PyMongo(app)

#loads login page and takes user to profile page if login details correct
@app.route('/index', methods=['GET','POST'])
def index():
    app.logger.info('Jade:Processing default request in app.py')
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('get_landing'))

    if request.method == 'GET':
        return render_template('index.html')

    if 'username' in session:
        return 'You are logged in as ' + session['USERNAME']

    return render_template("landing.html",
                            user=mongo.db.users.find())




#checks to see user login details exist/are correct and if correct returns user to cafes page
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    
    if login_user:
        #ERROR: you never defined bcrypt
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            # create a session cookie
            session['USERNAME'] = "me"
            session['USERNAME'] = request.form['username']
            return render_template('landing.html',
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
            session['USERNAME'] = request.form['username']
            return render_template('myprofile.html')
        
        return 'That username already exists!'

    return render_template('register.html')

#loads cafe page with all cafes in Mongo
@app.route('/get_landing')
def get_landing():
        result = session.get('USERNAME', None)
        if result:
            username = session['USERNAME']
            
            user=mongo.db.users.find_one({'name' : username})
            cafes=mongo.db.cafes.find()
            app.logger.info('User id is ' + str(user['_id']))
            user_id=user['_id']
            app.logger.info('cafes ' + str(cafes))
            return render_template("landing.html",
                                    user_id=user_id)

        # User not signed in
        return render_template('landing.html') 



#loads cafe page with all cafes in Mongo
@app.route('/get_cafes')
def get_cafes():
        result = session.get('USERNAME', None)
        if result:
            username = session['USERNAME']
            
            user=mongo.db.users.find_one({'name' : username})
            cafes=mongo.db.cafes.find()
            app.logger.info('User id is ' + str(user['_id']))
            user_id=user['_id']
            app.logger.info('cafes ' + str(cafes))
            return render_template("cafes.html",
                                cafes=cafes,user_id=user_id)

        # User not signed in
        return render_template('index.html') 


#loads each individual cafe page when see more button clicked
@app.route('/get_individualcafe/<cafe_id>/<user_id>')
def get_individualcafe(cafe_id,user_id):
        result = session.get('USERNAME', None)
        if result:
            username = session['USERNAME']
            app.logger.info('Username id is ' + username)
            cafe=mongo.db.cafes.find_one({'_id': ObjectId(cafe_id)})
            return render_template("individualcafe.html",cafe=cafe,user_id=user_id)

        # User not signed in
        return render_template('index.html')                     


#leaves user add review
@app.route('/add_review', methods=['POST'])
def add_review():
    result = session.get('USERNAME', None)
    if result:
        reviews = mongo.db.cafes.reviews
        reviews.insert_one( {"$set": {
            '0': request.form.get('review'),
            '1': request.form.get('username'),
        }})
        return redirect(url_for('get_profile'))

    # User not signed in
    return render_template('index.html')         


#loads user profile page if user logged in, if user not logged in loads log in page 
@app.route('/get_profile')
def get_profile():
        result = session.get('USERNAME', None)
        if result:
            username = session['USERNAME']
            return render_template("myprofile.html",
                                    cafes=mongo.db.cafes.find(), user_data=existing_user, 
                                    users_password=users_password)   
                # User not signed in
        return render_template('index.html') 




#logs user out 
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template("cafes.html",
                                cafes=mongo.db.cafes.find())

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

