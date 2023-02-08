from flask import Blueprint, render_template

from scripts.helpers import *

tabGroup1 = Blueprint("tabGroup1", __name__)

@tabGroup1.route("/addMealTab")
def addMealTab():
    return render_template("addMealTab.html")

@tabGroup1.route("/addFoodTab")
def addFoodTab():
    db = get_db()
    c = db.cursor()

    foodFormData = loadFoodFormData(c)

    category_nest = foodFormData["category_nest"]
    nutrient_nest = foodFormData["nutrient_nest"]

    db.close()
    return render_template(
        "addFoodTab.html",
        category_nest=category_nest,
        nutrient_nest=nutrient_nest,
    )

@tabGroup1.route("/manageFoodTab")
def manageFoodTab():
    return render_template("manageFoodTab.html")

@tabGroup1.route("/addComboTab")
def addComboTab():
    return render_template("addComboTab.html")

@tabGroup1.route("/manageComboTab")
def manageComboTab():
    return render_template("manageComboTab.html")

@tabGroup1.route("/addCategoryTab")
def addCategoryTab():
    return render_template("addCategoryTab.html")

@tabGroup1.route("/manageCategoryTab")
def manageCategoryTab():
    return render_template("manageCategoryTab.html")


    