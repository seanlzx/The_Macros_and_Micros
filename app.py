import sys
from contextlib import suppress
from datetime import datetime
from os import supports_bytes_environ

from flask import Flask, redirect, render_template, request

from scripts.helpers import *

DATABASE = "nutrition.db"

app = Flask(__name__)

# development variables, should eventually get rid of the hardcode
hardCodeUserId = 0
hardCodeDriGroupName = "male 19-30"


@app.teardown_appcontext
def close_connectioncall(exception):
    close_connection(exception)


@app.route("/addMeal", methods=["POST", "GET"])
def addMeal():
    c = get_db().cursor()
    return redirect("/")
    # ensure the format for hour and minute have zero padding


@app.route("/addFood", methods=["POST", "GET"])
def addFood():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        # processing of some data from the database that the below code may use
        categoryToIdDict = {}
        nutrientToIdDict = {}
        for category in c.execute("SELECT name, id FROM category"):
            categoryToIdDict[category[0]] = category[1]

        for nutrient in c.execute("SELECT name, id FROM nutrient"):
            nutrientToIdDict[nutrient[0]] = nutrient[1]

        # below is just retrieval from request adn a bit of validation
        infoKeyList = ["name", "description", "price"]
        infoDict = getFormListValues(infoKeyList)

        if not all(key in infoDict for key in ["name"]):
            return apology("Form insufficient info")

        categoryList = request.form.getlist("category")
        nutrientDict = getFormListValues(list(nutrientToIdDict.keys()))

        # below is the actual insert into SQL
        c.execute(
            """INSERT INTO food 
                 (timestamp, user_id, name, description,price) 
                 VALUES (?, ?, ?, ?, ?)""",
            (
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                hardCodeUserId,
                infoDict["name"],
                infoDict["description"],
                infoDict["price"],
            ),
        )

        food_id = c.lastrowid

        for category in categoryList:
            c.execute(
                """INSERT INTO food_to_category
                    (food_id, category_id) VALUES (?, ?)
                    """,
                (food_id, categoryToIdDict[category]),
            )

        for nutrient in nutrientDict:
            c.execute(
                """INSERT INTO food_to_nutrient
                    (food_id, nutrient_id, quantity) VALUES (?, ?, ?)
                    """,
                (food_id, nutrientToIdDict[nutrient], nutrientDict[nutrient]),
            )
    db.commit()
    db.close()

    # the page url will be /addFood which will cause route problems, so should do a redirect to index instead? yeap
    return redirect("/")


@app.route("/manageFoodSearchResults")
def manageFoodSearchResults():
    db = get_db()
    c = db.cursor()

    input = request.args.get("search")

    # early declaration just to ensure it's not unbound
    food_results = {}

    if input:
        raw_food_results = c.execute(
            "SELECT id, timestamp, name, description FROM food WHERE name LIKE ?",
            (f"%{input}%",),
        )

    else:
        raw_food_results = c.execute(
            "SELECT id, timestamp, name, description FROM food"
        )

    food_results = listOfTuplesToListOfDict(
        raw_food_results, ["id", "timestamp", "name", "description"]
    )

    for food in food_results:
        raw_categories = c.execute(
            """
            SELECT c.id AS id, c.name AS name
            FROM category c
            JOIN food_to_category ftc
            ON c.id = ftc.category_id
            WHERE ftc.food_id = ?;
            """,
            (food["id"],),
        )

        categories = listOfTuplesToListOfDict(raw_categories, ["id", "name"])
        food["categories"] = categories

        raw_nutrients = c.execute(
            """
            SELECT n.id AS id, n.name AS name, ftn.quantity AS quantity 
            FROM nutrient n
            JOIN food_to_nutrient ftn
            ON n.id = ftn.nutrient_id
            WHERE ftn.food_id = ?;                                             
            """,
            (food["id"],),
        )

        nutrients = listOfTuplesToListOfDict(raw_nutrients, ["id", "name", "quantity"])
        food["nutrients"] = nutrients

    db.close
    return render_template("manageFoodSearchResults.html", food_results=food_results)


@app.route("/manageFoodLoadEditor")
def manageFoodLoadEditor():
    db = get_db()
    c = db.cursor()

    foodFormData = loadFoodFormData()

    category_nest = foodFormData["category_nest"]
    nutrient_nest = foodFormData["nutrient_nest"]
    foodList = foodFormData["foodList"]
    categoryList = foodFormData["categoryList"]

    id = request.args.get("id")

    # if id:

    db.close
    return render_template(
        "manageFoodEditor.html",
        category_nest=category_nest,
        nutrient_nest=nutrient_nest,
        foodList=foodList,
        categoryList=categoryList,
    )


@app.route("/addCombo", methods=["POST", "GET"])
def addCombo():
    c = get_db().cursor()

    return redirect("/")


@app.route("/")
def index():

    foodFormData = loadFoodFormData()

    category_nest = foodFormData["category_nest"]
    nutrient_nest = foodFormData["nutrient_nest"]
    foodList = foodFormData["foodList"]
    categoryList = foodFormData["categoryList"]

    return render_template(
        "index.html",
        category_nest=category_nest,
        nutrient_nest=nutrient_nest,
        foodList=foodList,
        categoryList=categoryList,
    )
