import json
import pprint
from datetime import datetime

from flask import Blueprint, redirect, render_template, request

from scripts.helpers import *

# might just use render apology() instead?


food = Blueprint("food", __name__, template_folder="templates")


@food.route("/addFood", methods=["POST", "GET"])
def addFood():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        # processing of some data from the database that the below code may use
        categoryToIdDict = {}
        nutrientToIdDict = {}
        for category in c.execute("SELECT name, id FROM category"):
            categoryToIdDict[category[0]] = category[1]

        for nutrient in c.execute("SELECT name, id FROM nutrient"):
            nutrientToIdDict[nutrient[0]] = nutrient[1]

        # below is just retrieval from request and a bit of validation
        infoDict = getFormListValues(["name", "description", "price"])

        categoryList = request.form.getlist("category")
        nutrientDict = getFormListValues(list(nutrientToIdDict.keys()))

        # backend verification of data
        if not all(key in infoDict for key in ["name"]):
            return apology("Form insufficient info")

        if (
            not infoDict["price"]
            .replace(".", "", 1)
            .replace("e", "")
            .replace("-", "")
            .isdigit()
        ):
            return apology("Price has to be a number")
        if infoDict["price"] and  float(infoDict["price"]) < 0:
            return apology("Price has to be positive")

        for nutrient in nutrientDict:
            if nutrientDict[nutrient]:
                if (
                    not nutrientDict[nutrient]
                    .replace(".", "", 1)
                    .replace("e", "")
                    .replace("-", "")
                    .isdigit()
                ):
                    return apology(nutrient + " input was not valid")

            if nutrientDict[nutrient] and float(nutrientDict[nutrient]) < 0:
                return apology(nutrient + " can't be a negative number")

        # below is the actual insert into SQL
        c.execute(
            """INSERT INTO food 
                 (timestamp, user_id, name, description,price) 
                 VALUES (?, ?, ?, ?, ?)""",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                hardCodeUserId,
                infoDict["name"],
                infoDict["description"],
                infoDict["price"],
            ),
        )

        food_id = c.lastrowid

        for category in categoryList:
            c.execute(
                """INSERT INTO food_to_category
                    (food_id, category_id) VALUES (?, ?)
                    """,
                (food_id, categoryToIdDict[category]),
            )

        for nutrient in nutrientDict:
            if nutrientDict[nutrient]:
                c.execute(
                    """INSERT INTO food_to_nutrient
                        (food_id, nutrient_id, quantity) VALUES (?, ?, ?)
                        """,
                    (food_id, nutrientToIdDict[nutrient], nutrientDict[nutrient]),
                )
    db.commit()
    db.close()

    return redirect("/")


@food.route("/manageFood_searchResults")
def manageFood_searchResults():
    db = get_db()
    c = db.cursor()

    input = str(request.args.get("search")).split(" ")
    username = request.args.get("username")
    keywords = str(request.args.get("keywords")).split(" ")

    categories = request.args.getlist("categories[]")
    combos = request.args.getlist("combos[]")
    nutrients = request.args.getlist("nutrients[]")

    order = request.args.get("order")
    nutrient_for_sorting_value = request.args.get("nutrient_for_sorting_value")

    food_results = []

    sql_string_select = "SELECT f.id AS id, f.timestamp AS timestamp, f.name AS name, f.description AS description, f.price AS price, u.name AS username"
    header_list = [
        "id",
        "timestamp",
        "name",
        "description",
        "price",
        "username",
    ]

    sql_string_from = """
        FROM food f 
        JOIN user u 
        ON f.user_id = u.id 
        JOIN food_to_nutrient ftn ON f.id = ftn.food_id 
    """

    sql_string_where = "WHERE f.active = 1 "

    sql_string_group = "GROUP BY f.id "

    sql_string_HAVINGorAND = "HAVING"

    sql_string_order = ""

    parameters_list = []

    if input[0]:
        sql_string_where += "AND (f.name LIKE ? "
        parameters_list.append("%" + input[0] + "%")
        if len(input) > 1:
            for item in input[1:]:
                sql_string_where += "OR f.name LIKE ? "
                parameters_list.append("%" + item + "%")
        sql_string_where += ") "

    if keywords[0]:
        sql_string_where += "AND (f.description LIKE ? "
        parameters_list.append("%" + keywords[0] + "%")
        if len(keywords) > 1:
            for keyword in keywords[1:]:
                sql_string_where += "OR f.description LIKE ? "
                parameters_list.append("%" + keyword + "%")
        sql_string_where += ") "

    if categories:
        sql_string_from += "JOIN food_to_category ftc ON ftc.food_id = f.id "
        sql_string_where += "AND ftc.category_id in (?"
        parameters_list.append(int(categories[0]))
        for category in categories[1:]:
            sql_string_where += ", ?"
            parameters_list.append(int(category))
        sql_string_where += ") "
        sql_string_group += f"{sql_string_HAVINGorAND} COUNT(DISTINCT ftc.category_id) = {len(categories)} "
        sql_string_HAVINGorAND = "AND"

    if combos:
        sql_string_from += "JOIN combo_to_food cotc ON cotc.food_id = f.id "
        sql_string_where += "AND cotc.combo_id in (?"
        parameters_list.append(int(combos[0]))
        for combo in combos[1:]:
            sql_string_where += ", ?"
            parameters_list.append(int(combo))
        sql_string_where += ") "
        sql_string_group += (
            f"{sql_string_HAVINGorAND} COUNT(DISTINCT cotc.combo_id) = {len(combos)} "
        )
        sql_string_HAVINGorAND = "AND"

    if nutrients:
        sql_string_where += "AND ftn.nutrient_id in (?"
        parameters_list.append(int(nutrients[0]))
        for nutrient in nutrients[1:]:
            sql_string_where += ", ?"
            parameters_list.append(int(nutrient))
        sql_string_where += ") "
        sql_string_group += f"{sql_string_HAVINGorAND} COUNT(DISTINCT ftn.nutrient_id) = {len(nutrients)} "
        sql_string_HAVINGorAND = "AND"

    if username:
        sql_string_where += "AND u.name LIKE ? "
        parameters_list.append(username)

    if nutrient_for_sorting_value:
        nutrientToIdDict = {}
        for nutrient in c.execute("SELECT name, id FROM nutrient"):
            nutrientToIdDict[nutrient[0]] = nutrient[1]

        sql_string_select += """
        ,n.name AS nutrient_name
        ,ftn.quantity * (1/f.price) AS quantity_per_dollar
        ,ftn.quantity AS nutrient_per_100_grams
        ,ftn.quantity * (100/(SELECT quantity FROM food_to_nutrient WHERE food_id = f.id and nutrient_id = 0))  AS nutrient_per_kcal
        """

        sql_string_from += """
        JOIN nutrient n ON n.id = ftn.nutrient_id
        """

        sql_string_where += "AND n.id = ?"
        parameters_list.append(nutrientToIdDict[nutrient_for_sorting_value])
        
        header_list.extend(["nutrient_name",
            "quantity_per_dollar",
            "nutrient_per_100_grams",
            "nutrient_per_kcal"])

    if order == "newest":
        sql_string_order = "ORDER BY f.timestamp DESC"
    elif order == "oldest":
        sql_string_order = "ORDER BY f.timestamp"
    elif order == "a-z":
        sql_string_order = "ORDER BY f.name"
    elif order == "z-a":
        sql_string_order = "ORDER BY f.name DESC"
    elif order == "price_highest":
        sql_string_order = "ORDER BY f.price DESC"
    elif order == "price_lowest":
        sql_string_order = "ORDER BY f.price"

    elif order == "highest_nutrient_per_dollar":
        sql_string_order = "ORDER BY ftn.quantity * (1/f.price) DESC"
    elif order == "lowest_nutrient_per_dollar":
        sql_string_order = "ORDER BY ftn.quantity * (1/f.price)"

    elif order == "highest_nutrient_per_kcal":
        sql_string_order = "ORDER BY ftn.quantity * (100/(SELECT quantity FROM food_to_nutrient WHERE food_id = f.id and nutrient_id = 0)) DESC"
    elif order == "lowest_nutrient_per_kcal":
        sql_string_order = "ORDER BY ftn.quantity * (100/(SELECT quantity FROM food_to_nutrient WHERE food_id = f.id and nutrient_id = 0))"

    elif order == "highest_nutrient_per_gram":
        sql_string_order = "ORDER BY ftn.quantity DESC"
    elif order == "lowest_nutrient_per_gram":
        sql_string_order = "ORDER BY ftn.quantity"

    print("sql statement")
    print(sql_string_from + sql_string_where + sql_string_group + sql_string_order)
    print("tuple")
    print(tuple(parameters_list))

    raw_food_results = c.execute(
        sql_string_select
        + sql_string_from
        + sql_string_where
        + sql_string_group
        + sql_string_order,
        tuple(parameters_list),
    )

    # retrieve foods where name like
    # if input:
    #     raw_food_results = c.execute(
    #         """
    #         SELECT f.id AS id, f.timestamp AS timestamp, f.name AS name, f.description AS description, u.name AS username
    #         FROM food f
    #         JOIN user u
    #         ON f.user_id = u.id
    #         WHERE f.name LIKE ?
    #         AND f.active = 1
    #         """,
    #         (f"%{input}%",),
    #     )
    # # if no input, retrieve all foods
    # else:
    #     raw_food_results = c.execute(
    #         """
    #         SELECT f.id AS id, f.timestamp AS timestamp, f.name AS name, f.description AS description, u.name AS username
    #         FROM food f
    #         JOIN user u
    #         ON f.user_id = u.id
    #         WHERE f.active = 1
    #         """
    #     )

    food_results = listOfTuplesToListOfDict(raw_food_results, header_list)

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
    if food_results:
        return render_template("manageFood_searchResults.html", food_results=food_results)
    else:
        return render_template("search_produced_noResults.html")

@food.route("/manageFoodLoadEditor")
def manageFoodLoadEditor():
    # load form inputs (beware loadFoodFormData will reopen and close the database), fixed by opening and closing the database outside the funciton
    db = get_db()
    c = db.cursor()

    foodFormData = loadFoodFormData(c)

    category_nest = foodFormData["category_nest"]
    nutrient_nest = foodFormData["nutrient_nest"]

    db = get_db()
    c = db.cursor()

    id = str(request.args.get("id"))

    # find out why.replace('.','',1).isdigit is underlines
    if not id.replace(".", "", 1).isdigit():
        return apology("id was not a positive number")

    raw_information = c.execute(
        """
        SELECT id, name, description, price
        FROM food 
        WHERE id = ?;
        """,
        (id,),
    )
    food_data = listOfTuplesToListOfDict(
        raw_information, ["id", "name", "description", "price"]
    )[0]

    raw_categories = c.execute(
        """
        SELECT category_id
        FROM food_to_category
        WHERE food_id = ?;
        """,
        (id,),
    )
    food_data["categories"] = [category[0] for category in raw_categories]

    raw_nutrients = c.execute(
        """
        SELECT nutrient_id, quantity 
        FROM food_to_nutrient
        WHERE food_id = ?;                    
    """,
        (id,),
    )
    food_data["nutrients"] = {nutrient[0]: nutrient[1] for nutrient in raw_nutrients}

    ctp_sql_string = """
        SELECT parent_id, child_id 
        FROM category_to_parent
        WHERE parent_id NOT IN (SELECT id FROM category WHERE active = 0)
        AND child_id NOT IN (SELECT id FROM category WHERE active = 0)
    """

    category_to_parent = listOfTuplesToListOfDict(
        c.execute(ctp_sql_string), ["parent_id", "child_id"]
    )

    category_to_parent_dict = {}
    for row in category_to_parent:
        if row["child_id"] not in category_to_parent_dict:
            category_to_parent_dict[row["child_id"]] = [row["parent_id"]]
        else:
            category_to_parent_dict[row["child_id"]].append(row["parent_id"])

    db.close()
    return render_template(
        "manageFood_editor.html",
        category_nest=category_nest,
        nutrient_nest=nutrient_nest,
        food_data=food_data,
        ctp_json=json.dumps(category_to_parent_dict),
    )


@food.route("/manageFood_editor_submit", methods=["POST"])
def manageFood_editor_submit():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        # processing of some data from the database that the below code may use
        categoryToIdDict = {}
        nutrientToIdDict = {}
        for category in c.execute("SELECT name, id FROM category"):
            categoryToIdDict[category[0]] = category[1]

        for nutrient in c.execute("SELECT name, id FROM nutrient"):
            nutrientToIdDict[nutrient[0]] = nutrient[1]

        # below is just retrieval from request adn a bit of validation
        infoKeyList = ["id", "name", "description", "price"]
        infoDict = getFormListValues(infoKeyList)

        categoryList = request.form.getlist("category")
        nutrientDict = getFormListValues(list(nutrientToIdDict.keys()))

        # backend verification of data
        if not all(key in infoDict for key in ["name"]):
            return apology("Form insufficient info")

        if (
            not infoDict["price"]
            .replace(".", "", 1)
            .replace("e", "")
            .replace("-", "")
            .isdigit()
        ):
            return apology("Price has to be a number")
        if infoDict["price"] and float(infoDict["price"]) < 0:
            return apology("Price has to be positive")

        for nutrient in nutrientDict:
            if nutrientDict[nutrient]:
                if (
                    not nutrientDict[nutrient]
                    .replace(".", "", 1)
                    .replace("e", "")
                    .replace("-", "")
                    .isdigit()
                ):
                    return apology(nutrient + " input was not valid")
                
            if nutrientDict[nutrient] and float(nutrientDict[nutrient]) < 0:
                return apology(nutrient + " can't be a negative number")

        # if not all(nutrientDict[nutrient].replace('.','',1).replace('e','').replace('-','').isdigit() for nutrient in nutrientDict):

        c.execute(
            "DELETE FROM food WHERE id=?",
            (infoDict["id"],),
        )
        c.execute(
            "DELETE FROM food_to_category WHERE food_id=?",
            (infoDict["id"],),
        )
        c.execute(
            "DELETE FROM food_to_nutrient WHERE food_id=?",
            (infoDict["id"],),
        )

        # below is the actual insert into SQL
        c.execute(
            """INSERT INTO food 
                 (id, timestamp, user_id, name, description, price) 
                 VALUES (?, ?, ?, ?, ?, ?)""",
            (
                infoDict["id"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                hardCodeUserId,
                infoDict["name"],
                infoDict["description"],
                infoDict["price"],
            ),
        )

        food_id = c.lastrowid

        for category in categoryList:
            c.execute(
                """INSERT INTO food_to_category
                    (food_id, category_id) VALUES (?, ?)
                    """,
                (food_id, categoryToIdDict[category]),
            )

        for nutrient in nutrientDict:
            if nutrientDict[nutrient]:
                c.execute(
                    """INSERT INTO food_to_nutrient
                        (food_id, nutrient_id, quantity) VALUES (?, ?, ?)
                        """,
                    (food_id, nutrientToIdDict[nutrient], nutrientDict[nutrient]),
                )

    db.commit()
    db.close()

    return redirect("/")


@food.route("/manageFood_editor_deactivate", methods=["POST"])
def manageFood_editor_deactivate():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        c.execute(
            "UPDATE food SET active = 0 WHERE id = ?",
            (request.form.get("id"),),
        )

    db.commit()
    db.close()

    return redirect("/")
