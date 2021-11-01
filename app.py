import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env
from flask import jsonify


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_cooking")
def get_cooking():
    cooking = mongo.db.cooking.find()
    return render_template("cooking.html", cooking=cooking)


# registration
@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
         {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username not free, choose another one")
            return redirect(url_for("registration"))

        if len(request.form.get("username")) not in range(5, 11):
            flash(
                "Username should be between 5-10 character, please try again")
            return redirect(url_for("registration"))

        if len(request.form.get("password")) not in range(5, 11):
            flash(
                "Password should be between 5-10 character, please try again")
            return redirect(url_for("registration"))


        registration = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(registration)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("login", username=session["user"]))

    return render_template("registration.html")


# login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for("profile", username=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return render_template(url_for("login"))


@app.route("/logout")
def logout():
    # loggong out user, removing session cookie
    session.pop("user")
    return redirect(url_for("get_cooking"))


@app.route("/account")
def account():
    return render_template("account.html")


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        cook = {
            "img_url": request.form.get("img_url"),
            "category_name": request.form.get("category_name"),
            "recipe_title": request.form.get("recipe_title"),
            "cooking_time": request.form.get("cooking_time"),
            "tools": request.form.get("tools").split(","),
            "ingredients": request.form.get("ingredients").split(","),
            "description": request.form.get("description"),
            "created_by": session["user"]
        }
        mongo.db.cooking.insert_one(cook)
        flash("Recipe Successfully Created")
        return redirect(url_for("get_cooking"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_recipes.html", categories=categories)


@app.route("/edit_recipe/<cook_id>", methods=["GET", "POST"])
def edit_recipe(cook_id):
    if request.method == "POST":

        update = {
            "img_url": request.form.get("img_url"),
            "category_name": request.form.get("category_name"),
            "recipe_title": request.form.get("recipe_title"),
            "cooking_time": request.form.get("cooking_time"),
            "tools": request.form.get("tools").split(","),
            "ingredients": request.form.get("ingredients").split(","),
            "description": request.form.get("description"),
            "created_by": session["user"]
        }
        mongo.db.cooking.update({"_id": ObjectId(cook_id)}, update)
        flash("Recipe Successfully Edited")

    cook = mongo.db.cooking.find_one({"_id": ObjectId(cook_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_recipe.html"
    , cook=cook, categories=categories)


@app.route("/admin")
def admin():
    if "user" in session:
        current_user = mongo.db.users.find_one({"_id": ObjectId()})
        admin_user = mongo.db.cooking.find_one({"added_by": "user"})
        if current_user == admin_user:
            all_cooking = mongo.db.cooking.find()
            return render_template("admin.html", cooking=all_cooking)


# create, update, delete function
@app.route("/recipe/<cook_id>", methods=["GET", "UPDATE", "DELETE"])
@app.route("/recipe", methods=["POST"])
def manage_recipe(cook_id=None):
    print(request.method)
    cats = mongo.db.categories.find().sort("category_name", 1)
    if request.method == "GET":
        cook = mongo.db.cooking.find_one({"_id": ObjectId(cook_id)})
        return render_template("edit_recipe.html", cook=cook, cats=cats)
# create recipe section
    if request.method == "POST":
        print("image_url: " + str(request.form.get("image_url")))
        cook = {
            "image_url": request.form.get("image_url"),
            "category_name": request.form.get("category_name"),
            "recipe_title": request.form.get("recipe_title"),
            "cooking_time": request.form.get("cooking_time"),
            "tools": request.form.get("tools").split(","),
            "ingredients": request.form.get("ingredients").split(","),
            "description": request.form.get("description"),
            "created_by": session["user"]
        }
        mongo.db.cooking.insert_one(cook)
        flash("Recipe Successfully Created")
        return redirect(url_for("get_cooking"))
# update section
    if request.method == "UPDATE":

        update = {
            "image_url": request.form.get("image_url"),
            "category_name": request.form.get("category_name"),
            "recipe_title": request.form.get("recipe_title"),
            "cooking_time": request.form.get("cooking_time"),
            "tools": request.form.get("tools").split(","),
            "ingredients": request.form.get("ingredients").split(","),
            "description": request.form.get("description"),
            "created_by": session["user"]
        }
        mongo.db.cooking.update({"_id": ObjectId(cook_id)}, update)
        flash("Recipe Successfully Edited")

        cook = mongo.db.cooking.find_one({"_id": ObjectId(cook_id)})
        return render_template("edit_recipe.html", cook=cook, cats=cats)
# delete section
    if request.method == "DELETE":
        mongo.db.cooking.remove({"_id": ObjectId(cook_id)})
        flash("Recipe Successfully Deleted")
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)