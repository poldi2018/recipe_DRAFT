import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import base64
import requests
from werkzeug.security import check_password_hash, generate_password_hash
# from aux_methods import add_blank_recipe


#creating instance of Flask to have an app object
app = Flask(__name__)
#setting name of db, parse and assign system env variable
app.config["MONGO_DBNAME"] = 'bookbaseDRAFT'
app.config["MONGO_URI"] = os.getenv('MONGO_URI_BOOKBASE_DRAFT', 'mongodb://localhost')
#app secretkey
app.secret_key = os.getenv("COOKBOOK_SECRET_KEY")
#building upload url for imgbb with base url and API key 
imgbb_upload_url="https://api.imgbb.com/1/upload?key="+os.getenv('IMGBB_CLIENT_API_KEY')
#creating instance of Pymongo with app object to connect to MongoDB
mongo = PyMongo(app)


def add_blank_recipe(session):
    if not mongo.db.recipes.find_one({"username": session["username"], "title": "dummy"}):
        recipes= mongo.db.recipes
        blank_recipe = {
            "title": "dummy",
            "username": session["username"]
        }
        recipes.insert_one(blank_recipe)
        dummy_recipe_id=mongo.db.recipes.find_one({"username": session["username"], "title": "dummy"})
        return dummy_recipe_id
    else:
        dummy_recipe_id=mongo.db.recipes.find_one({"username": session["username"], "title": "dummy"})
    return dummy_recipe_id


# ROUTES AND VIEWS
#HEADER
@app.route('/reviews')
def reviews():
    reviews=mongo.db.reviews.find()
    return render_template("reviews.html", reviews=reviews)


@app.route('/advanced_search')
def advanced_search():
    return render_template("search.html")

@app.route('/results', methods=["POST"])
def results():
    return render_template("results.html")





#Create recipe
# one route to addrecipe dialog 



#registeration
@app.route('/register')
def register():
    userbase = mongo.db.users.find()
    return render_template('register.html', userbase=userbase)


@app.route('/insert_user', methods=["POST"])
def insert_user():
    users= mongo.db.users
    new_user = {
    "username": request.form.get('username'), 
    "email_address": request.form.get('email_address'),
    "password": generate_password_hash(request.form.get('password'))
    }
    users.insert_one(new_user)
    return redirect(url_for('failed_to_register', message="Provided email or username was not found!"))


@app.route('/login_page')
def login_page():
    return render_template("loginpage.html", message="Please login with your username and password. Thanks!")

    

@app.route('/check_user', methods=["POST"])
def check_user():
    #user_to_query= mongo.db.users.find_one({"email_address": request.form.get("email_address")})
    user_to_query= mongo.db.users.find_one( { '$or': [{"email_address": request.form.get("email_address")}, {"username": request.form.get("username")}]})
    password_response=check_password_hash(user_to_query['password'], request.form.get('password'))
    if user_to_query and password_response:
        session['username']=user_to_query['username']
        session['email_address']=user_to_query['email_address']
        print(session)
        return redirect(url_for('user', username=session["username"]))
    else:
        return render_template('loginpage.html', message="Username or password incorrect. Please try again.")


@app.route('/<username>')
def user(username):
    return render_template("homepage.html", username=username)

@app.route('/logout/<username>')
def logout(username):
    username_to_log_out=username
    print(session["username"])
    session["username"]=""
    print(session["username"])
    print(session["email_address"])

    return render_template("loggedout.html", username_to_log_out=username_to_log_out)





@app.route('/add_recipe')
def add_recipe():
    #check if a session object has been created
    if not session['username']:
        return render_template("loginpage.html", message="Please login first in order to be able to post recipes. Thanks!")
    else:
        return render_template('addrecipe.html', dummy_recipe_id=add_blank_recipe(session))

@app.route('/fileselector')
def fileselector(): 
    return render_template('fileselector.html')

@app.route('/file_uploader', methods=["POST"])
def file_uploader():
    # build upload URL string for imgbb with base url and API Key
    #https://ibb.co/album/hFMN1F
    response = requests.post(imgbb_upload_url, data={"image": request.form.get("base64file"), "album": "hFMN1F"})
    print(response.text)

    url_img_src=response.json()
    url_img_src=url_img_src["data"]["url"]
    return render_template("done.html", url_img_src=url_img_src)




#one route for inserting recipe into db
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipes= mongo.db.recipes
    recipe = {
    "title": request.form.get('recipe_title'), 
    "reviews": [{
        "rated_by": "me", 
        "stars": request.form.get('stars'),
        "comment": "good"
    }]}
    recipes.insert_one(recipe)
    return redirect(url_for('get_recipes'))


#Read from databse
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_recipes')
def get_recipes():
    recipes= mongo.db.recipes.find()
    return render_template('getrecipes.html', recipes=recipes)

@app.route('/latest_added')
def latest_added():
    return render_template("latest_added.html")


#Update database
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=recipe)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes=mongo.db.recipes
    new_rating = { 
        "rated_by": "her", 
        "stars": "99",
        "comment": "phenomenal"
    }
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        "title": request.form.get('recipe_title'), 
        "reviews": [{
        "rated_by": "me", 
        "stars": request.form.get('stars'),
        "comment": "good"}, new_rating]
    })
    return redirect(url_for('get_recipes'))

#Delete recipe in database
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

@app.route('/rate_recipe/<recipe_id>')
def rate_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('raterecipe.html', recipe=recipe)

@app.route('/insert_rating/<recipe_id>', methods=["POST"])
def insert_rating(recipe_id):
    recipe_to_rate = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    new_rating = { 
        "rated_by": "me", 
        "stars": request.form.get('stars'),
        "comment": request.form.get('comment')
    }
    
    #recipe_to_rate["reviews"].update(new_rating)
    #recipe_to_rate["reviews"].update(new_rating2)
    #print(recipe_to_rate["reviews"])
    recipe_to_rate.update(new_rating)
    return redirect(url_for('get_recipes'))

@app.route('/addformfield')
def addformfield():
    return render_template("addformfield.html")

@app.route('/insertformfield', methods=["POST"])
def insertformfield():
    testfield=request.form.get('formtestfield')
    categoryfield=request.form.get('category_name')
    print(categoryfield)
    print(testfield)
    return render_template("test.html", testfield=testfield, categoryfield=categoryfield)


# execution of app
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)