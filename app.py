import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime
import base64
import requests
from werkzeug.security import check_password_hash, generate_password_hash

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

mongo.db.recipes.create_index([("title", "text"), ("dish_type", "text"), ("level", "text"), ("directions", "text"), ("allergens", "text"), ("ingredients", "text"), ("origin", "text")])
mongo.db.reviews.create_index([("review_title", "text"), ("review_for", "text"), ("rating", "text"), ("comment", "text")])


def upload_image(base64file):
    response = requests.post(imgbb_upload_url, data={"image": base64file})
    url_img_src=response.json()
    url_img_src=url_img_src["data"]["url"]
    return url_img_src

def logout_user(session):
    session["username"]=""    
    session["user"]=""
    session["email_address"]=""

def set_session(user):
    session['username']=user['username']
    session['email_address']=user['email_address_hash']
    return session


#ROUTES AND VIEWS

#Indexpage CHECKED
@app.route('/')
def index():
    return render_template("index.html")

#HEADER
@app.route('/reviews')
def reviews():
    reviews=mongo.db.reviews.find()
    if not reviews:
        raise Exception("No reviews found")
    return render_template("reviews.html", reviews=reviews)

#Search dialog CHECKED
@app.route('/advanced_search')
def advanced_search():
    return render_template("search.html")

@app.route('/results', methods=["POST"])
def results():
    search_term=request.form.get("search_term")
    recipes=mongo.db.recipes.find({"$text":{"$search": search_term}})
    reviews=mongo.db.reviews.find({"$text":{"$search": search_term}})

    return render_template("results.html", recipes=recipes, reviews=reviews, search_term=search_term)

#registeration of user CHECKED 
@app.route('/register')
def register():
    return render_template('register.html', message='Please fill in the registration form.')

# check on registration request CHECKED
@app.route('/insert_user', methods=["POST"])
def insert_user():
    users= mongo.db.users
    user_email_to_check = mongo.db.users.find_one({"email_address": request.form.get('email_address')}) 
    username_to_check = mongo.db.users.find_one({"username": request.form.get('username')}) 

    if not user_email_to_check and not username_to_check: 
        new_user = {
            "username": request.form.get('username').casefold(), 
            "email_address": request.form.get('email_address'),
            "email_address_hash": generate_password_hash(request.form.get('email_address')),
            "password": generate_password_hash(request.form.get('password'))
        }
        users.insert_one(new_user)
        message="Account created! Please login with your username or email and password. Thanks!"
        return render_template("loginpage.html", message=message) 

    elif user_email_to_check:
        message="Provided email has already been registered. Please choose a different one."
        return render_template('register.html', message=message)

    elif username_to_check:
        message="Provided username has already been registered. Please choose a different one."
        return render_template('register.html', message=message)
    
    elif user_email_to_check and username_to_check:
        message="Provided email and username already have been registered."
        return render_template('register.html', message=message)

#login page CHECKED
@app.route('/login_page')
def login_page():
    message="Please login with your username and password. Thanks!"
    return render_template("loginpage.html", message=message)

# check on provided credentials CHECKED
@app.route('/check_credentials', methods=["POST"])
def check_credentials():
    user_email_to_check = mongo.db.users.find_one({"email_address": request.form.get('email_address')}) 
    username_to_check = mongo.db.users.find_one({"username": request.form.get('username').casefold()})
    #user_to_query= mongo.db.users.find_one( { '$or': [{"email_address_hash": generate_password_hash(request.form.get('email_address'))}, {"username": request.form.get("username")}]}) 
    if user_email_to_check:
        password_response=check_password_hash(user_email_to_check['password'], request.form.get('password'))
        if password_response:
            session=set_session(user_email_to_check) 
            return redirect(url_for("latest_added", session=session))

    elif username_to_check:
        password_response=check_password_hash(username_to_check['password'], request.form.get('password'))
        if password_response:
            session=set_session(username_to_check)
            return redirect(url_for("latest_added", session=session))

    return render_template('loginpage.html', message="Username or password incorrect. Please try again.")

# route to user's homepage CHECKED
@app.route('/home')
def home():
    recipes = mongo.db.recipes.find({"email_address_hash": session["email_address"]}) 
    return render_template('user.html', session=session, recipes=recipes)

# logout page CHECKED
@app.route('/logout')
def logout():
    logout_user(session)
    return redirect(url_for('latest_added'))

#Add A Recipe CHECKED
@app.route('/add_recipe')
def add_recipe():
    #check if user has been logged in and hence a session object has been created
    if not session['username']:
        return render_template("loginpage.html", message="Please login first to be able to post recipes. Thanks!")
    else:
        return render_template('addrecipe.html')

#Inserting recipe into db
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipes= mongo.db.recipes
    url_img_src=upload_image(request.form.get("base64file"))
    today = datetime.datetime.now().strftime("%d. %B %Y")
    now = datetime.datetime.now().strftime("%H:%M:%S")
    recipes.insert_one(
    {
        "title": request.form.get('recipe_title'), 
        "dish_type": request.form.get('dish_type'),
        "added_by": session["username"],
        "user_email_hash": session["email_address"],
        "added_on_date": today,
        "added_on_time": now,
        "edited_on_date": today,
        "edited_on_time": now,
        "level": request.form.get("level"),
        "review_count": 0,
        "view_count": 0,
        "prep_time": request.form.get("prep_time"),
        "cooking_time": request.form.get("cooking_time"),
        "total_time": request.form.get("prep_time")+request.form.get("cooking_time"),
        "directions": request.form.get("directions"),
        "allergens": request.form.get("allergens"),
        "ingredients": request.form.get("ingredients"),
        "origin": request.form.get("origin"),
        "img_src": url_img_src
    })
    return redirect(url_for('latest_added', session=session))

#Read recipe
@app.route('/read_recipe/<recipe_id>')
def read_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    reviews_of_recipe = mongo.db.reviews.find({"recipe_id": recipe_id})    
    #increment view counter
    recipes = mongo.db.recipes
    recipes.update_one({"_id": ObjectId(recipe_id)},
    {
        "$inc": {"view_count": 1 }
    })
    return render_template('readrecipe.html', recipe=recipe, reviews_of_recipe=reviews_of_recipe)

#show latest recipes
@app.route('/latest_added')
def latest_added():
    recipes=mongo.db.recipes.find()
    return render_template("latest_added.html", session=session, recipes=recipes)

#Update database CHECKED
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=recipe)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    url_img_src=upload_image(request.form.get("base64file"))
    today = datetime.datetime.now()
    now = datetime.datetime.now().strftime("%H:%M:%S")
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    recipes = mongo.db.recipes
    recipes.update_one({"_id": ObjectId(recipe_id)},
    {
        "$set":{ 
        "title": request.form.get('recipe_title'), 
        "dish_type": request.form.get('dish_type'),
        "added_by": session["username"],
        "user_email_hash": session["email_address"],
        "edited_on_date": today,
        "edited_on_time": now,
        "level": request.form.get("level"),
        "review_count": recipe["review_count"],
        "view_count": recipe["review_count"],
        "prep_time": request.form.get("prep_time"),
        "cooking_time": request.form.get("cooking_time"),
        "total_time": request.form.get("prep_time")+request.form.get("cooking_time"),
        "directions": request.form.get("directions"),
        "allergens": request.form.get("allergens"),
        "ingredients": request.form.get("ingredients"),
        "origin": request.form.get("origin"),
        "img_src": url_img_src
        }
    })
    return redirect(url_for('latest_added'))

#Delete recipe in database CHECKED
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
    #delete id from reviews!!
    return redirect(url_for('latest_added', session=session))


#Rate recipe
@app.route('/rate_recipe/<recipe_id>')
def rate_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('raterecipe.html', recipe_id=recipe_id, recipe_title=recipe['title'], added_by=recipe['added_by'])

#insert rating
@app.route('/insert_rating/<recipe_id>/<recipe_title>', methods=["POST"])
def insert_rating(recipe_id, recipe_title):
    reviews = mongo.db.reviews
    reviews.insert_one(
    {   "review_title": request.form.get('review_title'),
        "review_for": recipe_title,
        "recipe_id":  recipe_id,
        "rating": request.form.get('rating'),
        "comment": request.form.get('comment')
    })
    #incrementing review counter
    recipes = mongo.db.recipes
    recipes.update_one({"_id": ObjectId(recipe_id)},
    {
        "$inc": {"review_count": 1 }
    })
    return redirect(url_for('latest_added', session=session))

# run app
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)


"""
    {
        "title": request.form.get('recipe_title'), 
        "dish_type": request.form.get('dish_type'),
        "added_by": session["username"],
        "user_email_hash": session["email_address"],
        "edited_on_date": today,
        "edited_on_time": now,
        "level": request.form.get("level"),
        "review_count": recipe["review_count"],
        "view_count": recipe["review_count"],
        "prep_time": request.form.get("prep_time"),
        "cooking_time": request.form.get("cooking_time"),
        "total_time": request.form.get("prep_time")+request.form.get("cooking_time"),
        "directions": request.form.get("directions"),
        "allergens": request.form.get("allergens"),
        "ingredients": request.form.get("ingredients"),
        "origin": request.form.get("origin"),
        "img_src": url_img_src
    }
"""