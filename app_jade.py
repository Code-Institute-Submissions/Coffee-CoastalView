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
            return render_template("individualcafe.html",cafe=cafe,user_id=user_id
                                ,
                                #user_id=mongo.db.users.find_one({'username' : username}),
                                #users_review=mongo.db.cafes.reviews.find_one({'_1': ObjectId(user_id)})
                                )
        # User not signed in
        return render_template('index.html')                     


#loads user profile page if user logged in, if user not logged in loads log in page 
@app.route('/get_profile')
def get_profile():
        result = session.get('USERNAME', None)
        if result:
            username = session['USERNAME']
            return render_template("myprofile.html",
                                    cafes=mongo.db.cafes.find(), user_name=username)          
        
        # User not signed in
        return render_template('index.html')                                                      

#loads cafe page with all cafes in Mongo
@app.route('/')
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



#loads login page and takes user to profile page if login details correct
@app.route('/index', methods=['GET','POST'])
def index():
    app.logger.info('Jade:Processing default request in app.py')
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('get_cafes'))

    if request.method == 'GET':
        return render_template('index.html')

    if 'username' in session:
        return 'You are logged in as ' + session['USERNAME']

    return render_template("myprofile.html",
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
            session['USERNAME'] = request.form['username']
            cafes=mongo.db.cafes.find()
        return redirect(url_for('get_cafes'))
    return 'Invalid username/password combination'



    # GET request
    return render_template('sign-in.html', failf=False)

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


@app.route('/rate_cafe/<cafe_id>', methods=['POST'])
def rate_cafe(cafe_id):
    """ Updates the cafe rating and number of ratings

    :return
        Redirect to the individual cafe page
    """
    try:
        # calculate new rating
        cafes = mongo.db.cafes
        current_cafe = cafes.find_one({'_id': ObjectId(cafe_id)})
        calculated_rating_total = int(current_cafe['ratings_total']) + 1
        calculated_sum = int(current_cafe['ratings_sum']) + int(request.form.get('rating'))
        # rounded average for simplicity
        calculated_avg = round(calculated_sum / calculated_rating_total)
        # update record
        cafes.update_one({'_id': ObjectId(cafe_id)}, {"$set": {
            'ratings_total': calculated_rating_total,
            'ratings_sum': calculated_sum,
            'rating_avg': calculated_avg
        }}, upsert=True)

    except:
        # raises a 404 error if any of these fail
        return abort(404, description="Resource not found")
    return redirect(url_for('get_individualcafe', cafe_id=cafe_id))



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