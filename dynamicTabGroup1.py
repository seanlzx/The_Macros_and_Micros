import json

from flask import Blueprint, render_template

from scripts.helpers import *

dynamicTabGroup1 = Blueprint("dynamicTabGroup1", __name__)


@dynamicTabGroup1.route("/addMeal_tab")
def addMeal_tab():
    return render_template("addMeal_tab.html")


@dynamicTabGroup1.route("/addFood_tab")
def addFood_tab():
    db = get_db()
    c = db.cursor()

    foodFormData = loadFoodFormData(c)

    category_nest = foodFormData["category_nest"]
    nutrient_nest = foodFormData["nutrient_nest"]
    sql_string = """
        SELECT parent_id, child_id 
        FROM category_to_parent
        WHERE parent_id NOT IN (SELECT id FROM category WHERE active = 0)
        AND child_id NOT IN (SELECT id FROM category WHERE active = 0)
    """

    category_to_parent = listOfTuplesToListOfDict(
        c.execute(sql_string), ["parent_id", "child_id"]
    )

    category_to_parent_dict = {}
    for row in category_to_parent:
        if row["child_id"] not in category_to_parent_dict:
            category_to_parent_dict[row["child_id"]] = [row["parent_id"]]
        else:
            category_to_parent_dict[row["child_id"]].append(row["parent_id"])

    db.close()
    return render_template(
        "addFood_tab.html",
        category_nest=category_nest,
        nutrient_nest=nutrient_nest,
        ctp_json=json.dumps(category_to_parent_dict),
    )


@dynamicTabGroup1.route("/manageFood_tab")
def manageFood_tab():
    db = get_db()
    c = db.cursor()
    searchFilterInfo = loadSearchFilterInfo(c)
    db.close()
    
    #this is for the validation on nutrient sorting on front end with the hacky storing of nutrient list in a div
    nutrient_list = []
    nutrients_headers_nest = searchFilterInfo["nutrients_headers_nest"]
    for header in nutrients_headers_nest:
        for nutrient in header["nutrients"]:
            nutrient_list.append(nutrient["name"])
    
    return render_template(
        "manageFood_tab.html",
        categories_headers_nest=searchFilterInfo["categories_headers_nest"],
        combos=searchFilterInfo["combos"],
        nutrients_headers_nest= nutrients_headers_nest,
        nutrient_list = json.dumps(nutrient_list)
    )


@dynamicTabGroup1.route("/addCombo_tab")
def addCombo_tab():
    return render_template("addCombo_tab.html")


@dynamicTabGroup1.route("/manageCombo_tab")
def manageCombo_tab():
    return render_template("manageCombo_tab.html")


@dynamicTabGroup1.route("/addCategory_tab")
def addCategory_tab():
    db = get_db()
    c = db.cursor()

    foodFormData = loadFoodFormData(c)

    category_nest = foodFormData["category_nest"]

    db.close()
    return render_template("addCategory_tab.html", category_nest=category_nest)


@dynamicTabGroup1.route("/manageCategory_tab")
def manageCategory_tab():
    return render_template("manageCategory_tab.html")

@dynamicTabGroup1.route("/addNutrient_tab")
def addNutrient_tab():
    db = get_db()
    c = db.cursor()

    headers = listOfTuplesToListOfDict(c.execute("SELECT id, name FROM nutrient_header"), ["id", "name"])

    db.close()
    return render_template("addNutrient_tab.html", headers=headers)


@dynamicTabGroup1.route("/manageNutrient_tab")
def manageNutrient_tab():
    return render_template("manageNutrient_tab.html")

@dynamicTabGroup1.route("/addDri_tab")
def addDri_tab():
    db = get_db()
    c = db.cursor()

    foodFormData = loadFoodFormData(c)
    nutrient_nest = foodFormData["nutrient_nest"]
    
    db.close()
    return render_template("addDri_tab.html", nutrient_nest=nutrient_nest)


@dynamicTabGroup1.route("/manageDri_tab")
def manageDri_tab():
    return render_template("manageDri_tab.html")

@dynamicTabGroup1.route("/setting_tab")
def setting_tab():
    db = get_db()
    c = db.cursor()
    
    raw = c.execute("SELECT id, name, weight, height, gender, age, from_date, to_date, dri_group, user_type FROM user WHERE id = ?", (hardCodeUserId,),)
    setting = listOfTuplesToListOfDict(raw, ["id", "name", "weight", "height", "gender", "age", "from_date", "to_date", "dri_group", "user_type"])[0]
    
    db.close()
    return render_template("setting_tab.html", setting=setting)
