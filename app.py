from contextlib import suppress
from os import supports_bytes_environ

from flask import Flask, render_template, request

from scripts.helpers import *

DATABASE = 'nutrition.db'

app = Flask(__name__)

# development variables, should eventually get rid of the hardcode
userid = 0
driGroupName = 'male 19-30'

@app.teardown_appcontext
def close_connectioncall(exception):
    close_connection(exception)

@app.route("/addFood", methods=["POST", "GET"])
def addFood():
    if request.method == "POST":

        infoKeyList = [
            "name", "description", "currentPrice", "lowPrice", "highPrice"
        ]
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
        print(f'category: {categoryList}')

    return render_template("index.html")


@app.route("/")
def index():
    c = get_db().cursor()
    
    raw_category = c.execute('SELECT name, id FROM category')
    category_dict = listOfTuplesToListOfDict(raw_category, ['name','id'])
    
    raw_ctp = c.execute('SELECT p.id AS p_id, p.name AS p_name, c.id AS c_id, c.name AS c_name FROM category p, category c, category_to_parent ctp WHERE p.id = ctp.parent_id AND c.id = ctp.child_id;')
    ctp_dict = listOfTuplesToListOfDict(raw_ctp, ['parent_id', 'parent_name', 'child_id', 'child_name']) 
    
    # for child category get parent
    for category in category_dict:
        print(f"child: {category['name']}", end=' ')
        for ctp in ctp_dict:
            if ctp['child_id'] == category['id']:
                print(f"\tparent: {ctp['parent_name']}",end=' ')
        print('')        

    # find the best way to arrange the categories
    
    return render_template("index.html", category_dict=category_dict)


