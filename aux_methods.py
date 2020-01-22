from app import mongo, requests, imgbb_upload_url

def add_blank_recipe(session):
    if not mongo.db.recipes.find_one({"username": session["username"], "title": "dummy"}):
        recipes= mongo.db.recipes
        recipe = {
            "title": "dummy",
            "username": session["username"]
        }
        recipes.insert_one(recipe)
        recipe_id=mongo.db.recipes.find_one({"username": session["username"], "title": "dummy"})
        return recipe_id
    else:
        recipe_id=mongo.db.recipes.find_one({"username": session["username"], "title": "dummy"})
    return recipe_id

def upload_to_imgbb(base64file):
    response = requests.post(imgbb_upload_url, data={"image": base64file})
    url_img_src=response.json()
    url_img_src=url_img_src["data"]["url"]
    return url_img_src

