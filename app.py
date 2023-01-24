# pprint just to print things nicely
import pprint
import sys
from contextlib import suppress
from datetime import datetime
from os import supports_bytes_environ

from flask import Flask, redirect, render_template, request

from food import food
from scripts.helpers import *

DATABASE = "nutrition.db"

app = Flask(__name__)
app.register_blueprint(blueprint = food, url_prefix="")

# development variables, should eventually get rid of the hardcode
hardCodeUserId = 0
hardCodeDriGroupName = "male 19-30"


@app.teardown_appcontext
def close_connectioncall(exception):
    close_connection(exception)

@app.route("/")
def index():

    db = get_db()
    c = db.cursor()

    foodFormData = loadFoodFormData(c)

    category_nest = foodFormData["category_nest"]
    nutrient_nest = foodFormData["nutrient_nest"]
    foodList = foodFormData["foodList"]
    categoryList = foodFormData["categoryList"]

    db.close()
    return render_template(
        "index.html",
        category_nest=category_nest,
        nutrient_nest=nutrient_nest,
        foodList=foodList,
        categoryList=categoryList,
    )
