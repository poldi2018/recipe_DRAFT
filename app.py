import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import base64
import requests
from werkzeug.security import check_password_hash, generate_password_hash


#creating instance of Flask to have an app object
app = Flask(__name__)
#setting name of db, read and assign system env variable
app.config["MONGO_DBNAME"] = 'bookbaseDRAFT'
app.config["MONGO_URI"] = os.getenv('MONGO_URI_BOOKBASE_DRAFT', 'mongodb://localhost')
#IMGBB_CLIENT_API_KEY retrieval 
imgbb_upload_url="https://api.imgbb.com/1/upload?key="+os.getenv('IMGBB_CLIENT_API_KEY')
#creating instance of Pymongo with app object to connect to MongoDB
mongo = PyMongo(app)


# routes and views
#Create recipe
# one route to addrecipe dialog 


@app.route('/fileselector')
def fileselector(): 
    return render_template('fileselector.html')

@app.route('/file_uploader', methods=["POST"])
def file_uploader():
    # build upload URL string for imgbb with base url and API Key
    response = requests.post(imgbb_upload_url, data={"image": request.form.get("base64file")})
    print(response.text)

    url_img_src=response.json()
    url_img_src=url_img_src["data"]["url"]
    return render_template("done.html", url_img_src=url_img_src)

#registeration
@app.route('/register')
def register():
    userbase = mongo.db.users.find()
    return render_template('register.html', userbase=userbase)

@app.route

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
        session['user']=user_to_query['username']
        return render_template('userfound.html', user_to_query=user_to_query, message="Username and password correct!")
    else:
        return render_template('loginpage.html', message="Username or password incorrect. Please try again.")
 



def add_blank_recipe():
    recipes= mongo.db.recipes
    blank_recipe = {

    }
    recipes.insert_one(blank_recipe)


@app.route('/add_recipe')
def add_recipe():
    #recipe_id = add_blank_recipe()
    return render_template('addrecipe.html')

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
@app.route('/get_recipes')
def get_recipes():
    recipes= mongo.db.recipes.find()
    return render_template('getrecipes.html', recipes=recipes)


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
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
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