import os
import bcrypt
from flask import Flask, render_template, redirect, request, url_for, \
    session, abort, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# from flask_debugtoolbar import DebugToolbarExtension
# import logging

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'coffee_coastalview'
app.config['MONGO_URI'] = os.getenv('MONGO_URI',
                                    'mongodb+srv://JOS:Malteasers1!@cluster0.qn0az.mongodb.net/coffee_coastalview?retryWrites=true&w=majority'
                                    )

app.config["SECRET_KEY"] = os.environ.get('SESSION_SECRET')
app.secret_key = 'super secret key'
# app.config['SESSION_TYPE'] = 'filesystem'
# logging.basicConfig(level=logging.DEBUG)
# toolbar = DebugToolbarExtension(app)

mongo = PyMongo(app)


# loads cafe page with all cafes in Mongo

#@app.route('/')
@app.route('/get_landing')
def get_landing():
    result = session.get('USERNAME', None)
    cafes = mongo.db.cafes.find()
    # app.logger.info('User id is ' + str(user['_id']))
    app.logger.info('cafes ' + str(cafes))
    top_three= mongo.db.cafes.aggregate([{"$sort" :{"ratings_avg" :-1}},{ "$limit" : 3}])
    return render_template('landing.html',top_three=top_three)



# loads cafe page with all cafes in Mongo

@app.route('/get_cafes')
def get_cafes():
    result = session.get('USERNAME', None)
    if result:
        username = session['USERNAME']

        user = mongo.db.users.find_one({'name': username})
        if user:
            cafes = mongo.db.cafes.find()
            app.logger.info('User id is ' + str(user['_id']))
            user_id = user['_id']
            app.logger.info('cafes ' + str(cafes))
            return render_template('cafes.html', cafes=cafes,
                                user_id=user_id)
    else: #make them log in

        return render_template('index.html')


@app.route('/search_database', methods=['GET', 'POST'])
def search_database():
    if request.method == 'POST':
            result = session.get('USERNAME', None)
            if result:
                username = session['USERNAME']
                user = mongo.db.users.find_one({'name': username})
            if user:
                app.logger.info('Post called in search_database ')
                user_id = user['_id']
                search_terms =  request.form['search_terms']
                cafes = mongo.db.cafes.find( { "$text": { "$search" : search_terms, "$caseSensitive" : False } } )
                return render_template('searchresults.html', cafes=cafes,
                                user_id=user_id)

    return abort(404, description='search_database:Resource not found')

# loads each individual cafe page when see more button clicked

@app.route('/get_individualcafe/<cafe_id>/<user_id>')
def get_individualcafe(cafe_id, user_id):
    result = session.get('USERNAME', None)
    if result:
        username = session['USERNAME']
        cafes = mongo.db.cafes.find()
        count = cafes.count()
        #existing_review = mongo.db.cafes.find( { "_id" : ObjectId(cafe_id),"reviews.user_id" : ObjectId(user_id) } )
        existing_review = mongo.db.cafes.find_one(    { 
        "_id" : ObjectId(cafe_id),"reviews.user_id" : ObjectId(user_id) },
        { "reviews.details" : 1, "_id" : 0    })

        #for item in existing_review:
        #    app.logger.info('Item ' + str(item) )
        #    app.logger.info('Item ' + str(item) + ' er ' + str(item['reviews']))
        #    app.logger.info('Item ' + str(item) + ' er ' + str(item['reviews'][0]['details']))
        # app.logger.info('Item ' + str(existing_review) ) #+ ' er ' + str(existing_review['reviews'][0]['details']))

        #existing_review = list(existing_reviews)

        cafe = mongo.db.cafes.find_one({'_id': ObjectId(cafe_id)})
        users_reviews = mongo.db.cafes.find({'_id': ObjectId(cafe_id),
                'reviews.user_id': ObjectId(user_id)})
        users_favourites = mongo.db.cafes.find({ "_id" : ObjectId(cafe_id),"favourites.user_id" : ObjectId(user_id) })        
        count = users_reviews.count()
        app.logger.info(' reviews.user_id : ' + str(user_id)
                        + 'cafe_id : ' + str(cafe_id))

            # reviews=mongo.db.cafes.aggregate([{ "$lookup": { "from": "users" , "localField": "user_id", "foreignField" : "user_id", "as": "userdetails" }  }])

        return render_template('individualcafe.html', cafe=cafe,
                               user_id=user_id,
                               user_reviews=users_reviews,existing_review = existing_review,users_favourites=users_favourites)

                                # user_id=mongo.db.users.find_one({'username' : username}),
                                # users_review=mongo.db.cafes.reviews.find_one({'_1': ObjectId(user_id)})
        # User not signed in

    return render_template('index.html')


# loads user profile page if user logged in, if user not logged in loads log in page

@app.route('/get_profile')
def get_profile():
    result = session.get('USERNAME', None)
    if result:
        username = session['USERNAME']
        user = mongo.db.users.find_one({'name': username})

            # favourites = mongo.db.users.find({ '_id' : ObjectId(user['_id'])} , {'favourites' : 1})

        cafes = \
            mongo.db.cafes.find({'favourites.user_id': ObjectId(user['_id'
                                ])})
        my_reviews= \
            mongo.db.cafes.find( { "reviews.user_id" : ObjectId(user['_id']) } )

        app.logger.info('Cafes = ' + str(cafes.count()) + ' User id is '
                         + str(user['_id']) + ' favourites are '
                        + str(cafes) + " reviews are " + str(my_reviews.count()))
        return render_template('myprofile.html', cafes=cafes,
                               user_name=username, user_id=user['_id'],my_reviews=my_reviews)

        # User not signed in

    return render_template('index.html')


# loads login page and takes user to profile page if login details correct

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():


    if request.method == 'GET':
        app.logger.info('Post called in index ')
        return render_template('index.html')

    if 'username' in session:
        return 'You are logged in as ' + session['USERNAME']
    cafes = mongo.db.cafes.find()
    my_reviews= \
            mongo.db.cafes.find( { "reviews.user_id" : ObjectId(user['_id']) } )
    return render_template('myprofile.html', cafes,
                           user_name='not logged in',
                           user=mongo.db.users.find(),my_review=my_reviews)


# checks to see user login details exist/are correct and if correct returns user to cafes page

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session.pop('USERNAME', None)
        app.logger.info('Post called in login, removed USERNAME from cookies '
                        )

    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    form_password = request.form['pass'].encode('utf-8')

    if login_user:

        login_user_password = login_user['password']
        decrypted_password = bcrypt.hashpw(form_password,
        login_user_password)

        if decrypted_password == login_user_password:

            # create a session cookie

            session['USERNAME'] = request.form['username']
            cafes = mongo.db.cafes.find()
            top_three= mongo.db.cafes.aggregate([{"$sort" :{"ratings_avg" :-1}},{ "$limit" : 3}])
    else:

        return 'Invalid username/password combination'
    return render_template('landing.html',top_three=top_three)


@app.route('/edit_user')
def edit_user():
    username = session['USERNAME']
    user = mongo.db.users.find_one({'name': username})
    return render_template('edituser.html', user=user)


# checks to see user login details exist/are correct and if correct returns user to cafes page

@app.route('/update_user', methods=['POST'])
def update_user():
    if request.method == 'POST':
        app.logger.info('Post called in update_user ')

    username = request.form['user_name']
    user_id = request.form['user_id']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    password = request.form['user_password']
    hashpass = bcrypt.hashpw(request.form['user_password'].encode('utf-8'
                    ), bcrypt.gensalt())

    # app.logger.info('password encrypted is  ' + str(encryptted))

    mongo.db.users.update_one({'_id': user['_id']},
                              {'$set': {'name': username}}, upsert=True)
    mongo.db.users.update_one({'_id': user['_id']},
                              {'$set': {'password': hashpass}}, upsert=True)
    cafes = \
        mongo.db.cafes.find({'favourites.user_id': ObjectId(user_id)})
    my_reviews= \
            mongo.db.cafes.find( { "reviews.user_id" : ObjectId(user['_id']) } )
    return render_template('myprofile.html', cafes=cafes,
                           user_name=username, user_id=user_id,my_reviews=my_reviews)


# brings user to registration page

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username'
                ]})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'
                    ), bcrypt.gensalt())
            users.insert({'name': request.form['username'],
                         'password': hashpass})
            session['USERNAME'] = request.form['username']
            return render_template('cafes.html')

        return 'That username already exists!'

    return render_template('register.html')


# db.users.update({"name" : "JadeO"}, { $addToSet: { favourites: ObjectId("5f4bca9026e1755ced5287ba") }} )

@app.route('/add_favourite/<cafe_id>/<user_id>')
def add_favourite(cafe_id, user_id):
    """ Updates the user favourites

    :return
        Redirect to the individual cafe page on completion
    """

    try:

        username = session['USERNAME']
        cafes = mongo.db.cafes
        cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
        existing_review = mongo.db.cafes.find_one(    { 
        "_id" : ObjectId(cafe_id),"reviews.user_id" : ObjectId(user_id) },
        { "reviews.details" : 1, "_id" : 0    })
        app.logger.info('username = ' + str(username) + ' cafe_id= '
                        + str(cafe_id) + ' user_id= ' + str(user_id))
        cafes.update({'_id': ObjectId(cafe_id)},
                     {'$push': {'favourites': {'user_id': ObjectId(user_id),
                     'user_name': username}}})
        users_favourites = mongo.db.cafes.find({ "_id" : ObjectId(cafe_id),"favourites.user_id" : ObjectId(user_id) })        
        cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
        #flash("Added to your favourites!")
    except:

        # raises a 404 error if any of these fail

        return abort(404, description='Resource not found')
    return render_template('individualcafe.html', cafe=cafe,
                           user_id=user_id,existing_review = existing_review,users_favourites=users_favourites)


# db.users.update({"name" : "JadeO"}, { $addToSet: { favourites: ObjectId("5f4bca9026e1755ced5287ba") }} )

# requested cafe to be added to database

@app.route('/request_cafe', methods=['POST'])
def request_cafe():
    mongo.db.requested_cafes.insert_one(request.form.to_dict())
    top_three= mongo.db.cafes.aggregate([{"$sort" :{"ratings_avg" :-1}},{ "$limit" : 3}])
    return render_template('landing.html',top_three=top_three)


@app.route('/remove_favourite/<cafe_id>/<user_id>')
def remove_favourite(cafe_id, user_id):
    """ Removes the user favourites

    :return
        Redirect to the individual cafe page on completion
    """

    try:

        username = session['USERNAME']
        cafes = mongo.db.cafes
        cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
        app.logger.info('remove_favourite: username = ' + str(username)
                        + ' cafe_id= ' + str(cafe_id) + ' user_id= '
                        + str(user_id))
        cafes.update({'_id': ObjectId(cafe_id)},
                     {'$pull': {'favourites': {'user_id': ObjectId(user_id)}}})
        cafes = \
            mongo.db.cafes.find({'favourites.user_id': ObjectId(user_id)})
        my_reviews= \
            mongo.db.cafes.find( { "reviews.user_id" : ObjectId(user_id) } )
    except:

        # raises a 404 error if any of these fail

        return abort(404, description='Resource not found')
    return render_template('myprofile.html', cafes=cafes,
                           user_name=username, user_id=user_id,my_reviews=my_reviews)


@app.route('/rate_cafe/<cafe_id>/<user_id>', methods=['POST'])
def rate_cafe(cafe_id, user_id):
    """ Updates the cafe rating and number of ratings

    :return
        Redirect to the individual cafe page
    """

    try:

        # calculate new rating

        cafes = mongo.db.cafes
        cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
        new_rating = int(request.form.get('rating'))
        current_cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
        calculated_rating_total = int(current_cafe['ratings_total']) + 1
        calculated_sum = int(current_cafe['ratings_sum']) \
            + int(new_rating)
        existing_review = mongo.db.cafes.find_one(    { 
        "_id" : ObjectId(cafe_id),"reviews.user_id" : ObjectId(user_id) },
        { "reviews.details" : 1, "_id" : 0    })

        # rounded average for simplicity

        calculated_avg = round(calculated_sum / calculated_rating_total)

        # update record

        cafes.update_one({'_id': ObjectId(cafe_id)},
                         {'$set': {'ratings_total': calculated_rating_total,
                         'ratings_sum': calculated_sum,
                         'ratings_avg': calculated_avg}}, upsert=True)
        cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
        users_favourites = mongo.db.cafes.find({ "_id" : ObjectId(cafe_id),"favourites.user_id" : ObjectId(user_id) })        
    except:

        # raises a 404 error if any of these fail

        return abort(404, description='Resource not found')
    return render_template('individualcafe.html', cafe=cafe,
                           user_id=user_id,existing_review = existing_review,users_favourites=users_favourites)


# logs user out

@app.route('/logout')
def logout():
    session.pop('USERNAME', None)
    return render_template('index.html')




# leaves user add review

@app.route('/add_review/<cafe_id>/<user_id>', methods=['POST'])
def add_review(cafe_id, user_id):
    username = session['USERNAME']
    cafes = mongo.db.cafes
    details = request.form.get('details')
    cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
    existing_review = mongo.db.cafes.find_one(    { 
        "_id" : ObjectId(cafe_id),"reviews.user_id" : ObjectId(user_id) },
        { "reviews.details" : 1, "_id" : 0    })
    app.logger.info('Details = ' + str(details) + ' username = '
                    + str(username) + ' cafe_id= ' + str(cafe_id)
                    + ' user_id= ' + str(user_id))
    cafes.update({'_id': ObjectId(cafe_id)},
                 {'$push': {'reviews': {'user_id': ObjectId(user_id),
                 'user_name': username, 'details': details}}})
    cafe = cafes.find_one({'_id': ObjectId(cafe_id)})  # refresh the list
    users_favourites = mongo.db.cafes.find({ "_id" : ObjectId(cafe_id),"favourites.user_id" : ObjectId(user_id) })        
    return render_template('individualcafe.html', cafe=cafe,
                           user_id=user_id,existing_review = existing_review,users_favourites=users_favourites)

# leaves user update review

@app.route('/update_review/<cafe_id>/<user_id>', methods=['POST'])
def update_review(cafe_id, user_id):
    username = session['USERNAME']
    cafes = mongo.db.cafes
    details = request.form.get('details')
    cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
    
    app.logger.info('Details = ' + str(details) + ' username = '
                    + str(username) + ' cafe_id= ' + str(cafe_id)
                    + ' user_id= ' + str(user_id))
    cafes.update( {"_id" : ObjectId(cafe_id),
                    "reviews.user_id" : ObjectId(user_id)},
                    { "$set" : { "reviews.$.details" : details } } )  
    existing_review = mongo.db.cafes.find_one(    { 
        "_id" : ObjectId(cafe_id),"reviews.user_id" : ObjectId(user_id) },
        { "reviews.details" : 1, "_id" : 0    })              
    cafe = cafes.find_one({'_id': ObjectId(cafe_id)})  # refresh the list
    users_favourites = mongo.db.cafes.find({ "_id" : ObjectId(cafe_id),"favourites.user_id" : ObjectId(user_id) }) 
    return render_template('individualcafe.html', cafe=cafe,
                           user_id=user_id,existing_review = existing_review,users_favourites=users_favourites)


@app.route('/remove_review/<cafe_id>/<user_id>')
def remove_review(cafe_id, user_id):
    """ Removes the user review

    :return
        Redirect to the individual cafe page on completion
    """

    try:

        username = session['USERNAME']
        cafes = mongo.db.cafes
        cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
        existing_review = mongo.db.cafes.find_one(    { 
        "_id" : ObjectId(cafe_id),"reviews.user_id" : ObjectId(user_id) },
        { "reviews.details" : 1, "_id" : 0    })
        result = cafes.update({'_id': ObjectId(cafe_id)},
                              {'$pull': {'reviews': {'user_id': ObjectId(user_id)}}})
        app.logger.info('Result = ' + str(result) + ' username = '
                        + str(username) + ' cafe_id= ' + str(cafe_id)
                        + ' user_id= ' + str(user_id))
        cafe = cafes.find_one({'_id': ObjectId(cafe_id)})  # refresh the list
        users_favourites = mongo.db.cafes.find({ "_id" : ObjectId(cafe_id),"favourites.user_id" : ObjectId(user_id) })
    except:

        # raises a 404 error if any of these fail

        return abort(404, description='Resource not found')
    return render_template('individualcafe.html', cafe=cafe,
                           user_id=user_id,existing_review = existing_review,users_favourites=users_favourites)

app.debug = True

# app.run()

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
