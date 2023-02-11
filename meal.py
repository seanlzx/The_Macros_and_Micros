from datetime import datetime, timedelta


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)
from flask import Blueprint, redirect, render_template, request

from scripts.helpers import *

# this is hardcoded for now
hardCodeDriGroupName = "male 19-30"
hardCodeUserId = 0

meal = Blueprint("meal", __name__, template_folder="templates")

@meal.route("/addMeal_addFood_searchResults")
def addMeal_addFood_searchResults():
    db = get_db()
    c = db.cursor()

    input = request.args.get("search")

    # early declaration just to ensure it's not unbound
    food_results = {}

    # retrieve foods where name like
    if input:
        raw_food_results = c.execute(
            """
            SELECT f.id AS id, f.timestamp AS timestamp, f.name AS name, f.description AS description, u.name AS username 
            FROM food f 
            JOIN user u 
            ON f.user_id = u.id 
            WHERE f.name LIKE ?
            AND f.active = 1
            """,
            (f"%{input}%",),
        )
    # if no input, retrieve all foods
    else:
        raw_food_results = c.execute(
            """
            SELECT f.id AS id, f.timestamp AS timestamp, f.name AS name, f.description AS description, u.name AS username 
            FROM food f 
            JOIN user u 
            ON f.user_id = u.id
            WHERE f.active = 1
            """
        )

    food_results = listOfTuplesToListOfDict(
        raw_food_results, ["id", "timestamp", "name", "description", "username"]
    )

    for food in food_results:
        raw_categories = c.execute(
            """
            SELECT c.id AS id, c.name AS name
            FROM category c
            JOIN food_to_category ftc
            ON c.id = ftc.category_id
            WHERE ftc.food_id = ?;
            """,
            (food["id"],),
        )

        categories = listOfTuplesToListOfDict(raw_categories, ["id", "name"])
        food["categories"] = categories

        raw_nutrients = c.execute(
            """
            SELECT n.id AS id, n.name AS name, ftn.quantity AS quantity 
            FROM nutrient n
            JOIN food_to_nutrient ftn
            ON n.id = ftn.nutrient_id
            WHERE ftn.food_id = ?;                                             
            """,
            (food["id"],),
        )

        nutrients = listOfTuplesToListOfDict(raw_nutrients, ["id", "name", "quantity"])
        food["nutrients"] = nutrients

    db.close()
    return render_template("addMeal_addFood_searchResults.html", food_results=food_results)

@meal.route("/addMeal_addFood_selected")
def addMeal_addFood_selected():
    db = get_db()
    c = db.cursor()
    
    # load values, the conversion to string is not necessary but just to get rid of the stupid.replace('.','',1).isdigit() underline
    id = str(request.args.get("id"))

    print(f"id: {id}")
    
    raw_information = c.execute("""
        SELECT id, name
        FROM food 
        WHERE id = ?;
        """, (id,),)
    food_data = listOfTuplesToListOfDict(raw_information, ["id", "name"])[0]
    
    db.close()
    return render_template(
        "addMeal_addFood_selected.html",
        food_data = food_data
    )
    
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
# to do with loading DRIs
    
# to do with loading of meal data
    from_list = [int(date) for date in str(request.args.get("from")).split("-")]
    to_list = [int(date) for date in str(request.args.get("to")).split("-")]

    from_date = datetime(from_list[0], from_list[1], from_list[2])
    to_date = datetime(to_list[0], to_list[1], to_list[2])
    
    iso_date_list = [raw_date.strftime("%Y-%m-%d") for raw_date in daterange(from_date, to_date)]
    
    meals = {}
    # this is to avoid SQL injection attack, yeah I could make two separate executes for ASC and DESC but screw that
    order_sql = ""
    
    if order == "DESC":
        iso_date_list_reversed = iso_date_list[:]
        iso_date_list.reverse()
        for date in iso_date_list_reversed:
            raw_meals = c.execute(""" 
            SELECT id, name, description, time_of_meal FROM meal 
            WHERE active=1 AND user_id = ? AND time_of_meal LIKE ? ORDER BY time_of_meal DESC
            """,(hardCodeUserId, f"%{date}%") 
            )
            meals_list = listOfTuplesToListOfDict(raw_meals, ["id", "name", "description", "time_of_meal"])
            if meals_list:
                meals[date] = meals_list
    elif order == "ASC":
        for date in iso_date_list:
            raw_meals = c.execute(""" 
            SELECT id, name, description, time_of_meal FROM meal 
            WHERE active=1 AND user_id = ? AND time_of_meal LIKE ? ORDER BY time_of_meal
            """,(hardCodeUserId, f"%{date}%") 
            )
            meals_list = listOfTuplesToListOfDict(raw_meals, ["id", "name", "description", "time_of_meal"])
            if meals_list:
                meals[date] = meals_list

    for date in meals:
        for meal in meals[date]:
            raw_foods = c.execute(""" 
                SELECT f.id AS id, f.name AS name, mtf.quantity AS quantity, f.description AS description, f.price AS price
                FROM food f
                JOIN meal_to_food mtf
                ON f.id = mtf.food_id
                WHERE mtf.meal_id = ?;
            """, (meal["id"],))
            meal["foods"] = listOfTuplesToListOfDict(raw_foods, ["id", "name", "quantity", "description", "price"])
        
            for food in meal["foods"]: 
                raw_categories = c.execute(
                    """
                    SELECT c.id AS id, c.name AS name
                    FROM category c
                    JOIN food_to_category ftc
                    ON c.id = ftc.category_id
                    WHERE ftc.food_id = ?;
                    """,
                    (food["id"],),
                )

                categories = listOfTuplesToListOfDict(raw_categories, ["id", "name"])
                food["categories"] = categories
                
                
                raw_nutrients = c.execute(
                    """
                    SELECT n.id AS id, n.name AS name, ftn.quantity AS quantity 
                    FROM nutrient n
                    JOIN food_to_nutrient ftn
                    ON n.id = ftn.nutrient_id
                    WHERE ftn.food_id = ?;                                             
                    """,
                    (food["id"],),
                )
                
                nutrients = listOfTuplesToListOfDict(raw_nutrients, ["id", "name", "quantity"])
                food["nutrients"] = nutrients
        
    print(meals)
    db.close()
    return render_template("meal_records.html", meals=meals)