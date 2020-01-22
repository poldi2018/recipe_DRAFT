import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import base64
import requests
from werkzeug.security import check_password_hash, generate_password_hash
from aux_methods import add_blank_recipe, upload_to_imgbb

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

#registeration
@app.route('/register')
def register():
    return render_template('register.html', message='Please fill in the registration form.')

# check on registration request
@app.route('/insert_user', methods=["POST"])
def insert_user():
    users= mongo.db.users
    new_user = {
    "username": request.form.get('username'), 
    "email_address": request.form.get('email_address'),
    "password": generate_password_hash(request.form.get('password'))
    }
    if not mongo.db.users.find_one({"email_address": request.form.get("email_address")}): 
        users.insert_one(new_user)
        return render_template("loginpage.html", message="Account created! Please login with your username and password. Thanks!") 
    else:
        return render_template('register.html', message="Provided email has already been registered. Please choose another one.")

#login page
@app.route('/login_page')
def login_page():
    return render_template("loginpage.html", message="Please login with your username and password. Thanks!")

# check on provided credentials
@app.route('/check_credentials', methods=["POST"])
def check_credentials():
    user_to_query= mongo.db.users.find_one( { '$or': [{"email_address": request.form.get("email_address")}, {"username": request.form.get("username")}]}) 
    password_response=check_password_hash(user_to_query['password'], request.form.get('password'))
    if user_to_query and password_response:
        session['username']=user_to_query['username']
        session['email_address']=user_to_query['email_address']
        return redirect(url_for("latest_added", username=session["username"]))
    else:
        return render_template('loginpage.html', message="Username or password incorrect. Please try again.")

# route to user's homepage
@app.route('/<username>')
def user(username):
    return render_template("homepage.html")


@app.route('/logout') #### exception!!
def logout():
    print(session["username"])
    session["username"]=""
    print(session["username"])
    print(session["email_address"])
    return render_template('latest_added.html', username=session["username"])


#Add A Recipe
@app.route('/add_recipe')
def add_recipe():
    #check if user has been logged in and hence a session object has been created
    if not session['username']:
        return render_template("loginpage.html", message="Please login first in order to be able to post recipes. Thanks!")
    else:
        return render_template('addrecipe.html', recipe_id=add_blank_recipe(session))

#Inserting recipe into db
@app.route('/insert_recipe/<recipe_id>', methods=["POST"])
def insert_recipe(recipe_id):
    recipes= mongo.db.recipes
    url_img_src=upload_to_imgbb(request.form.get("base64file"))
    #response = requests.post(imgbb_upload_url, data={"image": request.form.get("base64file")})
    #url_img_src=response.json()
    #url_img_src=url_img_src["data"]["url"]
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        "title": request.form.get('recipe_title'), 
        "dish_type": request.form.get('dish_type'),
        "added_by:": session["username"],
        "user_email": session["email_address"],
        "img_src": url_img_src
    })
    return redirect(url_for('latest_added'))

#Route to indexpage
@app.route('/')
def index():
    return render_template("index.html")

#show latest recipes
@app.route('/latest_added')
def latest_added():
    recipes=mongo.db.recipes.find()
    return render_template("latest_added.html", recipes=recipes)

#Update database
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=recipe)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes=mongo.db.recipes
    """
    new_rating = { 
        "rated_by": "her", 
        "stars": "99",
        "comment": "phenomenal"
    }
    """
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        "title": request.form.get('recipe_title'), 
        "reviews": [{
        "rated_by": "me", 
        "stars": request.form.get('stars'),
        "comment": "good"}]
    })
    return redirect(url_for('get_recipes'))

#Delete recipe in database
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
    return redirect(url_for('latest_added'))

#Rate recipe
@app.route('/rate_recipe/<recipe_id>')
def rate_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('raterecipe.html', recipe=recipe)

#insert rating
@app.route('/insert_rating/<recipe_id>', methods=["POST"])
def insert_rating(recipe_id):
    recipe_to_rate = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    new_rating = { 
        "rated_by": "me", 
        "stars": request.form.get('stars'),
        "comment": request.form.get('comment')
    }
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

# run app
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)
