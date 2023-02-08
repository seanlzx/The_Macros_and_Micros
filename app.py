# pprint just to print things nicely

from flask import Flask, render_template

from food import food
from scripts.helpers import *
from tabGroup1 import tabGroup1

DATABASE = "nutrition.db"

app = Flask(__name__)
app.register_blueprint(blueprint = food, url_prefix="")
app.register_blueprint(blueprint = tabGroup1, url_prefix="")

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
