# pprint just to print things nicely
from pprint import pprint

from flask import Flask, render_template

from dynamicTabGroup1 import dynamicTabGroup1
from food import food
from meal import meal
from scripts.helpers import *

DATABASE = "nutrition.db"

app = Flask(__name__)
app.register_blueprint(blueprint = food, url_prefix="")
app.register_blueprint(blueprint = meal, url_prefix="")
app.register_blueprint(blueprint = dynamicTabGroup1, url_prefix="")

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
    
    foodList = [food[0] for food in c.execute("SELECT name FROM food WHERE active = 1")]
    categoryList = [category[0] for category in c.execute("SELECT name FROM category")]
    
    db.close()
    return render_template(
        "index.html",
        foodList = foodList,
        categoryList = categoryList
        )
