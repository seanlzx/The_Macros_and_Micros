# pprint just to print things nicely
from pprint import pprint

from flask import Flask, render_template

from category import category
from combo import combo
from dynamicTabGroup1 import dynamicTabGroup1
from food import food
from meal import meal
from scripts.helpers import *

DATABASE = "nutrition.db"

app = Flask(__name__)
app.register_blueprint(blueprint=food, url_prefix="")
app.register_blueprint(blueprint=meal, url_prefix="")
app.register_blueprint(blueprint=dynamicTabGroup1, url_prefix="")
app.register_blueprint(blueprint=combo, url_prefix="")
app.register_blueprint(blueprint=category, url_prefix="")

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
    comboList = [
        food[0] for food in c.execute("SELECT name FROM combo WHERE active = 1")
    ]
    users = listOfTuplesToListOfDict(c.execute("SELECT name FROM user WHERE active=1"), ["name"])

    db.close()
    return render_template(
        "index.html", foodList=foodList, categoryList=categoryList, comboList=comboList, users=users
    )


@app.route("/load_comboSearch")
def loadCombos():
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
        raw_food = c.execute(
            """
            SELECT f.id AS id, f.name AS name, ctf.quantity AS quantity, f.description AS description
            FROM food f
            JOIN combo_to_food ctf
            ON f.id = ctf.food_id
            WHERE ctf.combo_id = ?;
        """,
            (combo["id"],),
        )

        combo["foods"] = listOfTuplesToListOfDict(
            raw_food, ["id", "name", "quantity", "description"]
        )

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
                (
                    food["quantity"],
                    food["id"],
                ),
            )

            nutrients = listOfTuplesToListOfDict(
                raw_nutrients, ["id", "name", "quantity"]
            )
            food["nutrients"] = nutrients

            for nutrient in food["nutrients"]:
                if nutrient["id"] in combo["nutrients"]:
                    combo["nutrients"][nutrient["id"]] += nutrient["quantity"]
                else:
                    combo["nutrients"][nutrient["id"]] = nutrient["quantity"]

    nutrient_headers = listOfTuplesToListOfDict(
        c.execute("SELECT id, name FROM nutrient_header;"), ["id", "name"]
    )

    for header in nutrient_headers:
        raw_dri_list = c.execute(
            """
        SELECT n.id AS nutrient_id, n.name AS name, d.rda AS rda, d.ul AS ul, n.description AS description
        FROM nutrient n
        JOIN dri d
        ON n.id = d.nutrient_id
        WHERE n.nutrient_header_id = ?
        AND d.active = 1 AND n.active = 1
        AND d.group_name = ?;
        """,
            (header["id"], hardCodeDriGroupName),
        )
        header["nutrients"] = listOfTuplesToListOfDict(
            raw_dri_list, ["nutrient_id", "name", "rda", "ul", "description"]
        )

    db.close()
    return render_template(
        "combo_searchResults.html",
        combo_results=combo_results,
        nutrient_headers=nutrient_headers,
        foodForm_id=request.args.get("foodForm_id"),
        container_id=request.args.get("container_id"),
    )


@app.route("/combo_loadForm")
def combo_loadForm():
    db = get_db()
    c = db.cursor()

    combo = {}

    id = request.args.get("id")

    raw_information = c.execute(
        """
        SELECT id, name, description FROM combo WHERE id = ?                                    
    """,
        (id,),
    )
    combo = listOfTuplesToListOfDict(raw_information, ["id", "name", "description"])[0]

    raw_food = c.execute(
        """
            SELECT f.id AS id, f.name AS name, ctf.quantity AS quantity, f.description AS description
            FROM food f
            JOIN combo_to_food ctf
            ON f.id = ctf.food_id
            WHERE ctf.combo_id = ?;
        """,
        (combo["id"],),
    )

    combo["foods"] = listOfTuplesToListOfDict(
        raw_food, ["id", "name", "quantity", "description"]
    )

    # combo["nutrients"] = {}

    # for food in combo["foods"]:
    #     raw_nutrients = c.execute(
    #         """
    #         SELECT n.id AS id, n.name AS name, ftn.quantity * (?/100.0) AS quantity
    #         FROM nutrient n
    #         JOIN food_to_nutrient ftn
    #         ON n.id = ftn.nutrient_id
    #         WHERE ftn.food_id = ?;
    #         """,
    #         (
    #             food["quantity"],
    #             food["id"],
    #         ),
    #     )

    #     nutrients = listOfTuplesToListOfDict(raw_nutrients, ["id", "name", "quantity"])
    #     food["nutrients"] = nutrients

    #     for nutrient in food["nutrients"]:
    #         if nutrient["id"] in combo["nutrients"]:
    #             combo["nutrients"][nutrient["id"]] += nutrient["quantity"]
    #         else:
    #             combo["nutrients"][nutrient["id"]] = nutrient["quantity"]

    # nutrient_headers = listOfTuplesToListOfDict(
    #     c.execute("SELECT id, name FROM nutrient_header;"), ["id", "name"]
    # )

    # for header in nutrient_headers:
    #     raw_dri_list = c.execute(
    #         """
    #     SELECT n.id AS nutrient_id, n.name AS name, d.rda AS rda, d.ul AS ul, n.description AS description
    #     FROM nutrient n
    #     JOIN dri d
    #     ON n.id = d.nutrient_id
    #     WHERE n.nutrient_header_id = ?
    #     AND d.active = 1 AND n.active = 1
    #     AND d.group_name = ?;
    #     """,
    #         (header["id"], hardCodeDriGroupName),
    #     )
    #     header["nutrients"] = listOfTuplesToListOfDict(
    #         raw_dri_list, ["nutrient_id", "name", "rda", "ul", "description"]
    #     )

    db.close()
    return render_template(
        "combo_form.html",
        combo=combo,
        # nutrient_headers=nutrient_headers,
        foodForm_id=request.args.get("foodForm_id"),
    )


@app.route("/foodSearch")
def foodSearch():

    db = get_db()
    c = db.cursor()
    searchFilterInfo = loadSearchFilterInfo(c)
    db.close()

    return render_template(
        "foodSearch.html",
        categories_headers_nest=searchFilterInfo["categories_headers_nest"],
        combos=searchFilterInfo["combos"],
        nutrients_headers_nest=searchFilterInfo["nutrients_headers_nest"],
        foodForm_id=request.args.get("foodForm_id"),
        id=request.args.get("id")
    )

@app.route("/addFood_searchResults")
def addMeal_addFood_searchResults():
    db = get_db()
    c = db.cursor()

    input = str(request.args.get("search")).split(" ")
    username = request.args.get("username")
    keywords = str(request.args.get("keywords")).split(" ")
    
    categories = request.args.getlist("categories[]")
    combos = request.args.getlist("combos[]")
    nutrients = request.args.getlist("nutrients[]")
    
    order = request.args.get("order")

    # early declaration just to ensure it's not unbound
    food_results = {}

    sql_string_selectFrom = """
        SELECT f.id AS id, f.timestamp AS timestamp, f.name AS name, f.description AS description, u.name AS username 
        FROM food f 
        JOIN user u 
        ON f.user_id = u.id 
    """
    
    sql_string_where = "WHERE f.active = 1 "
    
    sql_string_group = "GROUP BY f.id "
    
    sql_string_HAVINGorAND = "HAVING"
    
    sql_string_order = ""
    
    parameters_list = []
    
    # the [0] is because the initial request is a string with .split(""), which even if the string is empty will lead to [""] which is considered a true condition
    if input[0]:
        sql_string_where += "AND (f.name LIKE ? "
        print("adding to sql query string input: ", input)
        parameters_list.append("%"+input[0]+"%")
        if len(input) > 1:
            for item in input[1:]:
                sql_string_where += "OR f.name LIKE ? "
                parameters_list.append("%"+item+"%")
        sql_string_where +=") "
                
    if keywords[0]:
        sql_string_where += "AND (f.description LIKE ? "
        print("adding to sql query string keywords: ", keywords)
        parameters_list.append("%"+keywords[0]+"%")
        if len(keywords) > 1:
            for keyword in keywords[1:]:
                sql_string_where += "OR f.description LIKE ? "
                parameters_list.append("%"+keyword+"%")
        sql_string_where +=") "
    
    if categories:
        sql_string_selectFrom += "JOIN food_to_category ftc ON ftc.food_id = f.id "
        sql_string_where += "AND ftc.category_id in (?"
        parameters_list.append(int(categories[0]))
        for category in categories[1:]:
            sql_string_where += ", ?"
            parameters_list.append(int(category))
        sql_string_where += ") "
        sql_string_group += f"{sql_string_HAVINGorAND} COUNT(DISTINCT ftc.category_id) = {len(categories)} "
        sql_string_HAVINGorAND = "AND"
            
    if combos:
        sql_string_selectFrom += "JOIN combo_to_food cotc ON cotc.food_id = f.id "
        sql_string_where += "AND cotc.combo_id in (?"
        parameters_list.append(int(combos[0]))
        for combo in combos[1:]:
            sql_string_where += ", ?"
            parameters_list.append(int(combo))
        sql_string_where += ") "
        sql_string_group += f"{sql_string_HAVINGorAND} COUNT(DISTINCT cotc.combo_id) = {len(combos)} "
        sql_string_HAVINGorAND = "AND"

    if nutrients:
        sql_string_selectFrom += "JOIN food_to_nutrient ftn ON ftn.food_id = f.id "
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
        print("adding to sql query string username: ", username)
        parameters_list.append(username)
        
    if order == "newest":
        sql_string_order = "ORDER BY f.timestamp DESC"
    elif order == "oldest":
        sql_string_order = "ORDER BY f.timestamp"
    elif order == "a-z":
        sql_string_order = "ORDER BY f.name"
    elif order == "z-a":      
        sql_string_order = "ORDER BY f.name DESC"

    print("sql statement")
    print(sql_string_selectFrom + sql_string_where + sql_string_group + sql_string_order)
    print("tuple")
    print(tuple(parameters_list))
    
    # is an empty tuple the possible cause of no results??????
    raw_food_results = c.execute(sql_string_selectFrom + sql_string_where + sql_string_group + sql_string_order, tuple(parameters_list))
    
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
    return render_template("addFood_searchResults.html", food_results=food_results)

@app.route("/addFood_selected")
def addFood_selected():
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
        "addFood_selected.html",
        food_data = food_data
    )