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

    # the page url will be /addFood which will cause route problems, so should do a redirect to index instead?
    return render_template("index.html")


@app.route("/")
def index():
    c = get_db().cursor()
    
    raw_header = c.execute('SELECT id, name FROM category_header')
    header_dict = listOfTuplesToListOfDict(raw_header, ['id', 'name'])
    
    raw_header_category_join = c.execute('''
        SELECT ch.id AS header_id, ch.name AS header, c.id AS category_id, c.name AS category
        FROM category c
        JOIN category_header ch
        ON c.category_header_id = ch.id;
        '''
    )
    header_category_join_dict = listOfTuplesToListOfDict(raw_header_category_join, ['header_id', 'header', 'category_id', 'category'])
    
    category_hierarchy = {}
    for header in header_dict:
        category_hierarchy[header['id']] = {'name':header['name'], 'category_list': []}

    for category in header_category_join_dict:
        category_hierarchy[category['header_id']]['category_list'].append({'id':category['category_id'], 'name':category['category']})
        
    print(category_hierarchy)
    
    # find the best way to arrange the categories
    
    return render_template("index.html", category_hierarchy=category_hierarchy)


