import pprint
from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request, url_for

from scripts.helpers import *

# this is hardcoded for now
hardCodeUserId = 0
hardCodeDriGroupName = "male 19-30"

combo = Blueprint("combo", __name__, template_folder="templates")

@combo.route("/addCombo", methods=["POST"])
def addCombo():
    db = get_db()
    c = db.cursor()
    
    if request.method == "POST":
        infoDict = getFormListValues(["name", "description"])
     
        if "name" not in infoDict:
            return apology("Please fill out a name")

        foodId_list = request.form.getlist("foodId")
        foodQuantity_list = request.form.getlist("foodQuantity")

        c.execute("INSERT INTO combo (timestamp, user_id, name, description) VALUES (?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), hardCodeUserId, infoDict["name"], infoDict["description"]),
        )

        combo_id = c.lastrowid

        for food_id, quantity in zip(foodId_list, foodQuantity_list):
            if not quantity.replace('.','',1).isdigit():
                return apology("quantity has to be a positive number")
            c.execute("INSERT INTO combo_to_food (combo_id, food_id, quantity) VALUES (?, ?, ?)",
                (combo_id, food_id, quantity)    
            )
        
    db.commit()
    db.close()
    return redirect("/")

@combo.route("/manageCombo_searchResults")
def manageCombo_searchResults():
    db = get_db()
    c = db.cursor()

    input = request.args.get("search")
    
    combo_results = {}
    
    if input:
        raw_combo_results = c.execute(
            """
            SELECT c.id AS id, c.timestamp AS timestamp, c.name AS name, c.description AS description, u.name AS username 
            FROM combo c 
            JOIN user u 
            ON c.user_id = u.id 
            WHERE c.name LIKE ?
            AND c.active = 1
            """,
            (f"%{input}%",),
        )
    else:
        raw_combo_results = c.execute(
            """
            SELECT c.id AS id, c.timestamp AS timestamp, c.name AS name, c.description AS description, u.name AS username 
            FROM combo c 
            JOIN user u 
            ON c.user_id = u.id 
            WHERE c.active = 1
            """
        )
        
    combo_results = listOfTuplesToListOfDict(
        raw_combo_results, ["id", "timestamp", "name", "description", "username"]
    )
    
    for combo in combo_results:
        raw_food = c.execute("""
            SELECT f.id AS id, f.name AS name, ctf.quantity AS quantity, f.description AS description
            FROM food f
            JOIN combo_to_food ctf
            ON f.id = ctf.food_id
            WHERE ctf.combo_id = ?;
        """, (combo["id"],),)
        
        combo["foods"] = listOfTuplesToListOfDict(raw_food, ["id", "name", "quantity", "description"])
        
        combo["nutrients"] = {}
        
        for food in combo["foods"]:
            raw_nutrients = c.execute(
                """
                SELECT n.id AS id, n.name AS name, ftn.quantity * (?/100.0) AS quantity 
                FROM nutrient n
                JOIN food_to_nutrient ftn
                ON n.id = ftn.nutrient_id
                WHERE ftn.food_id = ?;                                             
                """,
                (food["quantity"],food["id"],),
            )
            
            nutrients = listOfTuplesToListOfDict(raw_nutrients, ["id", "name", "quantity"])
            food["nutrients"] = nutrients
            
            for nutrient in food["nutrients"]:
                if nutrient["id"] in combo["nutrients"]:
                    combo["nutrients"][nutrient["id"]] += nutrient["quantity"]
                else:
                    combo["nutrients"][nutrient["id"]] = nutrient["quantity"] 
    
    nutrient_headers = listOfTuplesToListOfDict(c.execute("SELECT id, name FROM nutrient_header;"), ["id", "name"])
    
    for header in nutrient_headers:
        raw_dri_list = c.execute("""
        SELECT n.id AS nutrient_id, n.name AS name, d.rda AS rda, d.ul AS ul, n.description AS description
        FROM nutrient n
        JOIN dri d
        ON n.id = d.nutrient_id
        WHERE n.nutrient_header_id = ?
        AND d.active = 1 AND n.active = 1
        AND d.group_name = ?;
        """, (header["id"], hardCodeDriGroupName))
        header["nutrients"] = listOfTuplesToListOfDict(raw_dri_list, ["nutrient_id", "name", "rda", "ul", "description"])
     
    db.close()
    return render_template("manageCombo_searchResults.html", combo_results=combo_results, nutrient_headers= nutrient_headers)

@combo.route("/combo_LoadEditorForm")
def combo_LoadEditorForm():
    db = get_db()
    c = db.cursor()
    
    combo = {}
    
    id = request.args.get("id")
    
    raw_information = c.execute("""
        SELECT id, name, description FROM combo WHERE id = ?                                    
    """, (id,),)
    combo = listOfTuplesToListOfDict(raw_information, ["id", "name", "description"])[0]
    
    raw_food = c.execute("""
            SELECT f.id AS id, f.name AS name, ctf.quantity AS quantity, f.description AS description
            FROM food f
            JOIN combo_to_food ctf
            ON f.id = ctf.food_id
            WHERE ctf.combo_id = ?;
        """, (combo["id"],),)
        
    combo["foods"] = listOfTuplesToListOfDict(raw_food, ["id", "name", "quantity", "description"])
    
    combo["nutrients"] = {}
    
    for food in combo["foods"]:
        raw_nutrients = c.execute(
            """
            SELECT n.id AS id, n.name AS name, ftn.quantity * (?/100.0) AS quantity 
            FROM nutrient n
            JOIN food_to_nutrient ftn
            ON n.id = ftn.nutrient_id
            WHERE ftn.food_id = ?;                                             
            """,
            (food["quantity"],food["id"],),
        )
        
        nutrients = listOfTuplesToListOfDict(raw_nutrients, ["id", "name", "quantity"])
        food["nutrients"] = nutrients
        
        for nutrient in food["nutrients"]:
            if nutrient["id"] in combo["nutrients"]:
                combo["nutrients"][nutrient["id"]] += nutrient["quantity"]
            else:
                combo["nutrients"][nutrient["id"]] = nutrient["quantity"] 

    nutrient_headers = listOfTuplesToListOfDict(c.execute("SELECT id, name FROM nutrient_header;"), ["id", "name"])
    
    for header in nutrient_headers:
        raw_dri_list = c.execute("""
        SELECT n.id AS nutrient_id, n.name AS name, d.rda AS rda, d.ul AS ul, n.description AS description
        FROM nutrient n
        JOIN dri d
        ON n.id = d.nutrient_id
        WHERE n.nutrient_header_id = ?
        AND d.active = 1 AND n.active = 1
        AND d.group_name = ?;
        """, (header["id"], hardCodeDriGroupName))
        header["nutrients"] = listOfTuplesToListOfDict(raw_dri_list, ["nutrient_id", "name", "rda", "ul", "description"])

    db.close()
    return render_template("manageCombo_editor.html", combo=combo, nutrient_headers=nutrient_headers)

@combo.route("/editCombo", methods=["POST"])
def combo_edit():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        infoDict = getFormListValues(["id", "name", "description"])
        
        if not all(key in infoDict for key in ["id", "name"]):
            return apology("Form insufficient info")
        
        foodId_list = request.form.getlist("foodId")
        foodQuantity_list = request.form.getlist("foodQuantity")
        
        
        c.execute("DELETE FROM combo WHERE id = ?", (infoDict["id"],),)
        c.execute("DELETE FROM combo_to_food WHERE combo_id = ?", (infoDict["id"],),)
        
        c.execute("INSERT INTO combo (id, timestamp, user_id, name, description) VALUES (?, ?, ?, ?, ?)",
            (infoDict["id"],datetime.now().strftime("%Y-%m-%d %H:%M:%S"), hardCodeUserId, infoDict["name"], infoDict["description"]),
        )

        combo_id = c.lastrowid

        for food_id, quantity in zip(foodId_list, foodQuantity_list):
            if not quantity.replace('.','',1).isdigit():
                return apology("quantity has to be a positive number")
            c.execute("INSERT INTO combo_to_food (combo_id, food_id, quantity) VALUES (?, ?, ?)",
                (combo_id, food_id, quantity)    
            )
        
    db.commit()
    db.close()
    
    return redirect("/")
              
@combo.route("/combo_edit_deactivate", methods=["POST"])
def combo_edit_deactivate():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        c.execute("UPDATE combo SET active = 0 WHERE id = ?", (request.form.get("id"),),)
    
    db.commit()
    db.close()

    # the page url will be /addFood which will cause route problems, so should do a redirect to index instead? yeap
    return redirect("/")