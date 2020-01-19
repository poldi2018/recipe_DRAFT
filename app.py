import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import base64
import requests


#creating instance of Flask to have an app object
app = Flask(__name__)
#setting name of db, read and assign system env variable
app.config["MONGO_DBNAME"] = 'bookbaseDRAFT'
app.config["MONGO_URI"] = os.getenv('MONGO_URI_BOOKBASE_DRAFT', 'mongodb://localhost')
#IMGBB_CLIENT_API_KEY retrieval 
IMGBB_CLIENT_API_KEY = os.getenv('IMGBB_CLIENT_API_KEY')
#creating instance of Pymongo with app object to connect to MongoDB
mongo = PyMongo(app)

#def upload_image(img_path):
  #  curl --location --request POST "https://api.imgbb.com/1/upload?key={{IMGBB_CLIENT_API_KEY}}" --form "image=R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"



# routes and views
#Create recipe
# one route to addrecipe dialog 

"""
response = requests.post('https://www.googleapis.com/qpxExpress/v1/trips/search', headers=headers, params=params, data=data)
response = requests.post('https://api.imgbb.com/1/upload', key=IMGBB_CLIENT_API_KEY, )


"""

@app.route('/fileselector')
def fileselector(): 
    """
    #image = open('static/images/labor.jpg', 'rb')
    #image = open('static/images/eisberg.jpg', 'rb')
    image_read = image.read() 
    #image_64_encode = base64.encodebytes(image_read)
    #image_64_encode = base64.encodebytes(image_read)    
    #response = requests.post('https://api.imgbb.com/1/upload?key={{IMGBB_CLIENT_API_KEY}}', data=image_64_encode)
    #print(response)
    """
    return render_template('fileselector.html')

@app.route('/file_uploader', methods=["POST"])
def file_uploader():
    base64_image = request.form.get("base64file")
    print(base64_image)
    response = requests.post('https://api.imgbb.com/1/upload?key=44a47b2e80665b461c141f86770a7396', data={"image": base64_image})
    logg=response.text
    print(logg)
    return render_template("done.html", response=response)



@app.route('/add_recipe')
def add_recipe():
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
    mongo.db.categories.remove({'_id': ObjectId(recipe_id)})
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