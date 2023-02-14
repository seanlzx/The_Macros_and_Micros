import sqlite3
from datetime import datetime, timedelta
# pprint just to print things nicely
from pprint import pprint

from scripts.helpers import *

hardCodeDriGroupName = "male 19-30"

def tupleToDict(tuple, listOfKeys):
    dict = {}
    for key, item in zip(listOfKeys, tuple):
        dict[key] = item
    return dict

def listOfTuplesToListOfDict(listOfTuples, listOfKeys):
    list = []
    for tuple in listOfTuples:
        list.append(tupleToDict(tuple, listOfKeys))
    return list

sqliteConnection = ""

try:
    order = "ASC"
    
    sqliteConnection = sqlite3.connect("nutrition.db")
    c = sqliteConnection.cursor()
    
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
    
    from_list = [int(date) for date in "2023-01-01".split("-")]
    to_list = [int(date) for date in "2024-01-01".split("-")]

    from_date = datetime(from_list[0], from_list[1], from_list[2])
    to_date = datetime(to_list[0], to_list[1], to_list[2])
    
    iso_date_list = [raw_date.strftime("%Y-%m-%d") for raw_date in daterange(from_date, to_date)]
    
    meals = {}
    # this is to avoid SQL injection attack, yeah I could make two separate executes for ASC and DESC but screw that
    order_sql = ""

    if order == "DESC":
        iso_date_list.reverse()
        for date in iso_date_list:
            raw_meals = c.execute(""" 
            SELECT id, name, description, time_of_meal FROM meal 
            WHERE active=1 AND user_id = ? AND time_of_meal LIKE ? ORDER BY time_of_meal DESC
            """,(hardCodeUserId, f"%{date}%") 
            )
            meals_list = listOfTuplesToListOfDict(raw_meals, ["id", "name", "description", "time_of_meal"])
            if meals_list:
                meals[date] = {"meals":meals_list}
    elif order == "ASC":
        for date in iso_date_list:
            raw_meals = c.execute(""" 
            SELECT id, name, description, time_of_meal FROM meal 
            WHERE active=1 AND user_id = ? AND time_of_meal LIKE ? ORDER BY time_of_meal
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
    print("pooop")
    print(meals)


except sqlite3.Error as error:
    print(error)
    
finally:
    if sqliteConnection:
        sqliteConnection.close()
