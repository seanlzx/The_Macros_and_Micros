from contextlib import suppress
from os import supports_bytes_environ

from flask import Flask, render_template, request

from scripts.helpers import *

DATABASE = "nutrition.db"

app = Flask(__name__)

# development variables, should eventually get rid of the hardcode
userid = 0
driGroupName = "male 19-30"


@app.teardown_appcontext
def close_connectioncall(exception):
    close_connection(exception)

@app.route("/addMeal", methods=['POST','GET'])
def addMeal():
    return render_template('index.html')
    #ensure the format for hour and minute have zero padding

@app.route("/addFood", methods=["POST", "GET"])
def addFood():
    if request.method == "POST":

        infoKeyList = ["name", "description", "currentPrice", "lowPrice", "highPrice"]
        infoDict = getFormListValues(infoKeyList)

        nutritionKeyList = [
            "calories",
            "carbohydrates",
            "proteins",
            "fiber",
            "total_fats",
            "monounsaturated_fats",
            "polyunsaturated_fats",
            "saturated_fats",
            "trans_fats",
            "omega_3",
            "vitamin_a",
            "vitamin_b1",
            "vitamin_b2",
            "vitamin_b3",
            "vitamin_b5",
            "vitamin_b6",
            "vitamin_b12",
            "vitamin_D",
            "vitamin_E",
            "vitamin_k",
            "choline",
            "folic_acid",
            "calcium",
            "chloride",
            "chromium",
            "copper",
            "fluoride",
            "iodine",
            "iron",
            "magnesium",
            "manganese",
            "phosphorus",
            "potatssium",
            "selenium",
            "sodium",
            "sulfur",
            "zinc",
            "cholestrol",
            "creatine",
            "caffeine",
            "good_bacteria",
            "mercury",
            "nitrates_and_nitrites",
            "Artificial_food_colors",
        ]
        nutritionDict = getFormListValues(nutritionKeyList)

        # get checkbox values
        categoryList = request.form.getlist("category")
        print(infoDict)
        print(nutritionDict)
        print(f"category: {categoryList}")

    # the page url will be /addFood which will cause route problems, so should do a redirect to index instead?
    return render_template("index.html")

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
    header_nutrient_dri_join_dict_list = listOfTuplesToListOfDict(
        raw_header_nutrient_dri_join_list,
        ["header_id", "id", "name", "description", "group_name", "rda", "ul"],
    )

    nutrient_nest = header_nesting(
        header_dict_list,
        header_nutrient_dri_join_dict_list,
        ["id", "name", "description", "group_name", "rda", "ul"],
    )
    
    print("ppop")
    print(nutrient_nest)

    return render_template("index.html", category_nest=category_nest, nutrient_nest=nutrient_nest)
