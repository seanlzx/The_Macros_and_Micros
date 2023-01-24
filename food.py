# pprint just to print things nicely
import pprint
import sys
from contextlib import suppress
from datetime import datetime
from os import supports_bytes_environ

from flask import Blueprint, abort, redirect, render_template, request
# might just use render apology() instead?
from jinja2 import TemplateNotFound

from scripts.helpers import *

food = Blueprint("food", __name__, template_folder="templates")

@food.route("/addFood", methods=["POST", "GET"])
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
        
        categoryList = request.form.getlist("category")
        nutrientDict = getFormListValues(list(nutrientToIdDict.keys()))

        # backend verification of data
        if not all(key in infoDict for key in ["name"]):
            return apology("Form insufficient info")
        
        if not infoDict["price"].replace('.','',1).isdigit():
            return apology("Price has to be a positive number")
        
        if not all(nutrientDict[nutrient].replace('.','',1).isdigit() for nutrient in nutrientDict):
            return apology("Nutrient Input has to be a positive number")

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


@food.route("/manageFoodSearchResults")
def manageFoodSearchResults():
    db = get_db()
    c = db.cursor()

    input = request.args.get("search")

    # early declaration just to ensure it's not unbound
    food_results = {}

    # retrieve foods where name like
    if input:
        raw_food_results = c.execute(
            """
            SELECT f.id AS id, f.timestamp AS timestamp, f.name AS name, f.description AS description, u.name AS username 
            FROM food f 
            JOIN user u 
            ON f.user_id = u.id 
            WHERE f.name LIKE ?
            """,
            (f"%{input}%",),
        )
    # if no input, retrieve all foods
    else:
        raw_food_results = c.execute(
            """
            SELECT f.id AS id, f.timestamp AS timestamp, f.name AS name, f.description AS description, u.name AS username 
            FROM food f 
            JOIN user u 
            ON f.user_id = u.id
            """
        )

    food_results = listOfTuplesToListOfDict(
        raw_food_results, ["id", "timestamp", "name", "description", "username"]
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

    db.close()
    return render_template("manageFoodSearchResults.html", food_results=food_results)


@food.route("/manageFoodLoadEditor")
def manageFoodLoadEditor():
    # load form inputs (beware loadFoodFormData will reopen and close the database), fixed by opening and closing the database outside the funciton
    db = get_db()
    c = db.cursor()
    
    foodFormData = loadFoodFormData(c)

    category_nest = foodFormData["category_nest"]
    nutrient_nest = foodFormData["nutrient_nest"]
    foodList = foodFormData["foodList"]
    categoryList = foodFormData["categoryList"]

    db = get_db()
    c = db.cursor()

    # load values, the conversion to string is not necessary but just to get rid of the stupid.replace('.','',1).isdigit() underline
    id = str(request.args.get("id"))

    print(f"id: {id}")

    # find out why.replace('.','',1).isdigit is underlines
    if not id.replace('.','',1).isdigit():
        return apology("id was not a positive number")
    
    raw_information = c.execute("""
        SELECT id, name, description, price
        FROM food 
        WHERE id = ?;
        """, (id,),)
    food_data = listOfTuplesToListOfDict(raw_information, ["id", "name", "description", "price"])[0]
    
    raw_categories = c.execute("""
        SELECT category_id
        FROM food_to_category
        WHERE food_id = ?;
        """, (id,),)
    food_data["categories"] = [category[0] for category in raw_categories]
    
    raw_nutrients = c.execute("""
        SELECT nutrient_id, quantity 
        FROM food_to_nutrient
        WHERE food_id = ?;                    
    """, (id,),)
    food_data["nutrients"] = {nutrient[0]: nutrient[1] for nutrient in raw_nutrients}
    pprint.pprint(food_data)
    
    db.close()
    return render_template(
        "manageFoodEditor.html",
        category_nest=category_nest,
        nutrient_nest=nutrient_nest,
        foodList=foodList,
        categoryList=categoryList,
        food_data = food_data
    )


@food.route("/manageFood_editor_submit", methods=["POST"])
def manageFood_editor_submit():
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
        infoKeyList = ["id", "name", "description", "price"]
        infoDict = getFormListValues(infoKeyList)
        
        categoryList = request.form.getlist("category")
        nutrientDict = getFormListValues(list(nutrientToIdDict.keys()))

        # backend verification of data
        if not all(key in infoDict for key in ["name"]):
            return apology("Form insufficient info")
        
        if not infoDict["price"].replace('.','',1).isdigit():
            return apology("Price has to be a positive number")
        
        if not all(nutrientDict[nutrient].replace('.','',1).isdigit() for nutrient in nutrientDict):
            return apology("Nutrient Input has to be a positive number")

        c.execute("DELETE FROM food WHERE id=?", (infoDict["id"],),)
        c.execute("DELETE FROM food_to_category WHERE food_id=?", (infoDict["id"],),)
        c.execute("DELETE FROM food_to_nutrient WHERE food_id=?", (infoDict["id"],),)

        # below is the actual insert into SQL
        c.execute(
            """INSERT INTO food 
                 (id, timestamp, user_id, name, description, price) 
                 VALUES (?, ?, ?, ?, ?, ?)""",
            (
                infoDict["id"],
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
