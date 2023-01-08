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

# made into a global variable so index() can fill the list, and addFood() can use it, yea pretty hackyy
nutritionKeyList = []

@app.teardown_appcontext
def close_connectioncall(exception):
    close_connection(exception)

@app.route("/addMeal", methods=['POST','GET'])
def addMeal():
    c = get_db().cursor()
    return redirect("/")
    #ensure the format for hour and minute have zero padding

@app.route("/addFood", methods=["POST", "GET"])
def addFood():
    c = get_db().cursor()
    if request.method == "POST":

        infoKeyList = ["name", "description", "price"]
        infoDict = getFormListValues(infoKeyList)

        # find a way to 
        if not all(key in infoDict for key in ["name", "description"]):
            return apology("Form insufficient info")
            
        nutritionDict = getFormListValues(nutritionKeyList)

        categoryList = request.form.getlist("category")
        print(f"infoDict: {infoDict}")
        print(f"category: {categoryList}")
        print(f"nutritionDict: {nutritionDict}")

        # quite simply check that infoDict has all the keys required
        c.execute("""INSERT INTO food 
                (timestamp, user_id, name, description,price) 
                VALUES (?, ?, ?, ?, ?)""", 
                (datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                hardCodeUserId, infoDict['name'], infoDict['description'])

    # the page url will be /addFood which will cause route problems, so should do a redirect to index instead? yeap
    return redirect("/")

@app.route("/addCombo", methods=["POST", "GET"])
def addCombo():
    c = get_db().cursor()
    
    return redirect("/")

@app.route("/")
def index():
    c = get_db().cursor()
    
    # produce category_hierarchy
    raw_header_list = c.execute("SELECT id, name FROM category_header")
    header_dict_list = listOfTuplesToListOfDict(raw_header_list, ["id", "name"])

    raw_header_category_join_list = c.execute(
        """
            SELECT ch.id AS header_id, c.id AS category_id, c.name AS category
            FROM category c
            JOIN category_header ch
            ON c.category_header_id = ch.id;
        """
    )
    header_category_join_dict_list = listOfTuplesToListOfDict(
        raw_header_category_join_list, ["header_id", "id", "name"]
    )

    category_nest = header_nesting(
        header_dict_list, header_category_join_dict_list, ["id", "name"]
    )

    # produce nutrient_hierarchy
    raw_header_list = c.execute("SELECT id, name FROM nutrient_header")
    header_dict_list = listOfTuplesToListOfDict(raw_header_list, ["id", "name"])

    raw_header_nutrient_dri_join_list = c.execute(
        """
            SELECT nh.id AS header_id, n.id AS id, n.name AS name, n.description AS description, 
            dri.group_name AS group_name, dri.rda AS rda, dri.ul AS ul
            FROM nutrient n
            JOIN nutrient_header nh
            ON n.nutrient_header_id = nh. id
            JOIN dri
            ON n.id = dri.nutrient_id; 
            """
    )
    
    print()
    header_nutrient_dri_join_dict_list = listOfTuplesToListOfDict(
        raw_header_nutrient_dri_join_list,
        ["header_id", "id", "name", "description", "group_name", "rda", "ul"],
    )

    nutrient_nest = header_nesting(
        header_dict_list,
        header_nutrient_dri_join_dict_list,
        ["id", "name", "description", "group_name", "rda", "ul"],
    )
    
    for group in nutrient_nest:
        for list in nutrient_nest[group]['list']:
            nutritionKeyList.append(list['name'])

    return render_template("index.html", category_nest=category_nest, nutrient_nest=nutrient_nest)
