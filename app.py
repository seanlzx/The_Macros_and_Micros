import sqlite3
from contextlib import suppress
from os import supports_bytes_environ

from flask import Flask, render_template, request

from scripts.helpers import getFormListValues

app = Flask(__name__)

# development variables, should eventually get rid of the hardcode
userid = 0
driGroupName = 'male 19-30'

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
    return render_template("index.html")
