import pprint
from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request

from scripts.helpers import *

# this is hardcoded for now

hardCodeUserId = 0

meal = Blueprint("meal", __name__, template_folder="templates")
    
@meal.route("/addMeal", methods=["POST"])
def addMeal():
    db = get_db()
    c = db.cursor()
    
    if request.method == "POST":
        infoDict = getFormListValues(["name", "description", "date", "hour", "minute"])
        
        if not all(key in infoDict for key in ["name", "date", "hour", "minute"]):
            return apology("Form insufficient info")
        
        date_list = str(infoDict["date"]).split("-")
        
        try:
            time_of_meal = str(datetime(
                    int(date_list[0]), 
                    int(date_list[1]), 
                    int(date_list[2]), 
                    int(infoDict["hour"]), 
                    int(infoDict["minute"])
                ).strftime("%Y-%m-%d %H:%M:%S"))
        except:
            return apology("Date or time are invalid")

        foodId_list = request.form.getlist("foodId")
        foodQuantity_list = request.form.getlist("foodQuantity")

        # time validation for hour and minutes, should already be settled above so
        # the below might not be needed
        # should sitll ensure that quantity is positive?, the below should be good enough

        try:
            if not infoDict["hour"].replace('.','',1).isdigit():
                return apology("hour has to be a positive number")
            if not infoDict["minute"].replace('.','',1).isdigit():
                return apology("minute has to be a positive number")
        except:
            # this might not be necessary cause the if not all(...) already checked that the above values are present
            return apology("User did not submit a necessary field")

        c.execute("INSERT INTO meal (timestamp, user_id, name, description, time_of_meal) VALUES (?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), hardCodeUserId, infoDict["name"], infoDict["description"], time_of_meal),
        )

        meal_id = c.lastrowid

        for food_id, quantity in zip(foodId_list, foodQuantity_list):
            if not quantity.replace('.','',1).isdigit():
                return apology("quantity has to be a positive number")
            c.execute("INSERT INTO meal_to_food (meal_id, food_id, quantity) VALUES (?, ?, ?)",
                (meal_id, food_id, quantity)    
            )
        
    db.commit()
    db.close()
    return redirect("/")


@meal.route("/meal_sort/<order>")
def meal_sort(order):
    db = get_db()
    c = db.cursor()
# to do with loading of meal data
    from_list = [int(date) for date in str(request.args.get("from")).split("-")]
    to_list = [int(date) for date in str(request.args.get("to")).split("-")]

    from_date = datetime(from_list[0], from_list[1], from_list[2])
    to_date = datetime(to_list[0], to_list[1], to_list[2])
    
    iso_date_list = [raw_date.strftime("%Y-%m-%d") for raw_date in daterange(from_date, to_date)]
    
    meals = {}
    order_sql = ""
    
    if order == "DESC":
        iso_date_list.reverse()
        order_sql = "DESC"

    for date in iso_date_list:
        raw_meals = c.execute(f""" 
        SELECT id, name, description, time_of_meal FROM meal 
        WHERE active=1 AND user_id = ? AND time_of_meal LIKE ? ORDER BY time_of_meal {order_sql}
        """,(hardCodeUserId, f"%{date}%") 
        )
        meals_list = listOfTuplesToListOfDict(raw_meals, ["id", "name", "description", "time_of_meal"])
        if meals_list:
            meals[date] = {"meals":meals_list}

    for date in meals:
        
        meals[date]["nutrients"] = {}
        
        for meal in meals[date]["meals"]:
            raw_foods = c.execute(""" 
                SELECT f.id AS id, f.name AS name, mtf.quantity AS quantity, f.description AS description, f.price AS price
                FROM food f
                JOIN meal_to_food mtf
                ON f.id = mtf.food_id
                WHERE mtf.meal_id = ?;
            """, (meal["id"],))
            meal["foods"] = listOfTuplesToListOfDict(raw_foods, ["id", "name", "quantity", "description", "price"])
        
            meal["nutrients"] = {}
        
            for food in meal["foods"]: 
                # # not really making use of food's categories in meal view, so commented out for now
                # raw_categories = c.execute(
                #     """
                #     SELECT c.id AS id, c.name AS name
                #     FROM category c
                #     JOIN food_to_category ftc
                #     ON c.id = ftc.category_id
                #     WHERE ftc.food_id = ?;
                #     """,
                #     (food["id"],),
                # )

                # categories = listOfTuplesToListOfDict(raw_categories, ["id", "name"])
                # food["categories"] = categories
                
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
                    if nutrient["id"] in meal["nutrients"]:
                        meal["nutrients"][nutrient["id"]] += nutrient["quantity"]
                    else:
                        meal["nutrients"][nutrient["id"]] = nutrient["quantity"]
                
            # what a f headache, next time, plan your data structures simpler, never use a dictionary as you would use a list, so stupid
            for nutrient in meal["nutrients"]:
                if nutrient in meals[date]["nutrients"]:
                    meals[date]["nutrients"][nutrient] += meal["nutrients"][nutrient]
                else: 
                    meals[date]["nutrients"][nutrient] = meal["nutrients"][nutrient]
# to do with loading nutrient_headers, nutrients details and DRIs
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
        """, (header["id"], get_dri_group(c)))
        header["nutrients"] = listOfTuplesToListOfDict(raw_dri_list, ["nutrient_id", "name", "rda", "ul", "description"])
                
    db.close()
    if meals:
        return render_template("meal_records.html", meals=meals, nutrient_headers=nutrient_headers)
    else:
        return render_template("search_produced_noResults.html")

@meal.route("/meal_loadEditForm")
def meal_loadEditForm():
    db = get_db()
    c = db.cursor()
    
    meal = {}
    
    id = request.args.get("id")
    
    raw_information = c.execute("""
        SELECT id, name, description, time_of_meal FROM meal WHERE id = ?; 
    """, (id,))
    meal = listOfTuplesToListOfDict(raw_information, ["id", "name", "description", "time_of_meal"])[0]
    
    # the form has date, hour and minute inputs, separate time_of_meal into such
    meal["date"] = meal["time_of_meal"].split(" ")[0]
    meal["hour"] = meal["time_of_meal"].split(" ")[1].split(":")[0]
    meal["minute"] = meal["time_of_meal"].split(" ")[1].split(":")[1]
    
    raw_foods = c.execute("""
        SELECT mtf.food_id AS id, f.name AS name, mtf.quantity AS quantity
        FROM meal_to_food mtf JOIN food f
        ON mtf.food_id = f.id
        WHERE meal_id = ?;
    """, (id,))
    meal["foods"] = listOfTuplesToListOfDict(raw_foods, ["id", "name", "quantity"])
    
    db.close()
    return render_template("meal_editForm.html", meal=meal)

@meal.route("/meal_edit", methods=["POST"])
def meal_edit():
    db = get_db()
    c = db.cursor()
    
    if request.method == "POST":
        infoDict = getFormListValues(["id", "name", "description", "date", "hour", "minute"])
        
        if not all(key in infoDict for key in ["id", "name", "date", "hour", "minute"]):
            return apology("Form insufficient info")
        
        date_list = str(infoDict["date"]).split("-")
        
        try:
            time_of_meal = str(datetime(
                    int(date_list[0]), 
                    int(date_list[1]), 
                    int(date_list[2]), 
                    int(infoDict["hour"]), 
                    int(infoDict["minute"])
                ).strftime("%Y-%m-%d %H:%M:%S"))
        except:
            return apology("Date or time are invalid")

        foodId_list = request.form.getlist("foodId")
        foodQuantity_list = request.form.getlist("foodQuantity")

        # time validation for hour and minutes, should already be settled above so
        # the below might not be needed
        # should sitll ensure that quantity is positive?, the below should be good enough

        try:
            if not infoDict["hour"].replace('.','',1).isdigit():
                return apology("hour has to be a positive number")
            if not infoDict["minute"].replace('.','',1).isdigit():
                return apology("minute has to be a positive number")
        except:
            # this might not be necessary cause the if not all(...) already checked that the above values are present
            return apology("User did not submit a necessary field")

        c.execute("DELETE FROM meal WHERE id = ?", (infoDict["id"],),)
        c.execute("DELETE FROM meal_to_food WHERE meal_id = ?", (infoDict["id"],),)

        c.execute("INSERT INTO meal (id, timestamp, user_id, name, description, time_of_meal) VALUES (?, ?, ?, ?, ?, ?)",
            (infoDict["id"],datetime.now().strftime("%Y-%m-%d %H:%M:%S"), hardCodeUserId, infoDict["name"], infoDict["description"], time_of_meal),
        )

        meal_id = c.lastrowid

        for food_id, quantity in zip(foodId_list, foodQuantity_list):
            if not quantity.replace('.','',1).isdigit():
                return apology("quantity has to be a positive number")
            c.execute("INSERT INTO meal_to_food (meal_id, food_id, quantity) VALUES (?, ?, ?)",
                (meal_id, food_id, quantity)    
            )
        
    db.commit()
    db.close()
    return redirect("/")

@meal.route("/meal_edit_deactivate", methods=["POST"])
def meal_edit_deactivate():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        c.execute("UPDATE meal SET active = 0 WHERE id = ?", (request.form.get("id"),),)
        
    db.commit()
    db.close()

    # the page url will be /addFood which will cause route problems, so should do a redirect to index instead? yeap
    return redirect("/")