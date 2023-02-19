import pprint
from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request, url_for

from scripts.helpers import *

# this is hardcoded for now
hardCodeUserId = 0
hardCodeDriGroupName = "male 19-30"

category = Blueprint("category", __name__, template_folder="templates")


@category.route("/addCategory", methods=["POST"])
def addCategory():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        categoryToIdDict = {}
        headerToIdDict = {}
        for category in c.execute("SELECT name, id FROM category"):
            categoryToIdDict[category[0]] = category[1]

        for header in c.execute("SELECT name, id FROM category_header"):
            headerToIdDict[header[0]] = header[1]

        name = request.form.get("name")

        header = request.form.get("header")

        parent_list = request.form.getlist("parent")

        c.execute(
            "INSERT INTO category (timestamp, name, category_header_id, user_id) VALUES (?, ?, ?, ?)",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                name,
                headerToIdDict[header],
                hardCodeUserId,
            ),
        )

        category_id = c.lastrowid

        for parent in parent_list:
            c.execute(
                "INSERT INTO category_to_parent (parent_id, child_id) VALUES (?, ?)",
                (categoryToIdDict[parent], category_id),
            )

    db.commit()
    db.close
    return redirect("/")


@category.route("/manageCategory_searchResults")
def manageCategory_searchResults():
    db = get_db()
    c = db.cursor()

    input = request.args.get("search")

    category_results = {}

    print(input)

    raw_category_results = ()
    if input:
        raw_category_results = c.execute(
            """
            SELECT c.id AS id, c.timestamp AS timestamp, c.name AS name 
            ,ch.id AS category_header_id, ch.name AS header_name, u.name AS username
            FROM category c
            JOIN category_header ch
            ON c.category_header_id = ch.id
            JOIN user u
            ON c.user_id = u.id
            WHERE c.active = 1
            AND c.name LIKE ?;                              
            """,
            (f"%{input}%",),
        )
        print(raw_category_results)
    else:
        raw_category_results = c.execute(
            """
            SELECT c.id AS id, c.timestamp AS timestamp, c.name AS name,
            ch.id AS category_header_id, ch.name AS header_name, u.name AS username
            FROM category c
            JOIN category_header ch
            ON c.category_header_id = ch.id
            JOIN user u
            ON c.user_id = u.id
            WHERE c.active = 1;
            """
        )

    category_results = listOfTuplesToListOfDict(
        raw_category_results,
        ["id", "timestamp", "name", "category_header_id", "header_name", "username"],
    )
    print(category_results)

    for category in category_results:
        raw_parent = c.execute(
            """
            SELECT ctp.parent_id AS id, c.name AS name 
            FROM category_to_parent ctp
            JOIN category c
            ON c.id = ctp.parent_id
            WHERE ctp.child_id = ?;
        """,
            (category["id"],),
        )

        category["parents"] = listOfTuplesToListOfDict(raw_parent, ["id", "name"])

    print(category_results)

    db.close()
    return render_template(
        "manageCategory_searchResults.html", category_results=category_results
    )

@category.route("/manageCategoryLoadEditor")
def manageCategoryLoadEditor():
    # load form inputs (beware loadFoodFormData will reopen and close the database), fixed by opening and closing the database outside the funciton
    db = get_db()
    c = db.cursor()

    foodFormData = loadFoodFormData(c)
    category_nest = foodFormData["category_nest"]

    id = str(request.args.get("id"))

    if not id.replace('.','',1).isdigit():
        return apology("id was not a positive number")

    raw_information = c.execute("""
        SELECT id, name, category_header_id
        FROM category
        WHERE id = ?;
        """, (id,),)
    category_data = listOfTuplesToListOfDict(raw_information, ["id", "name", "category_header_id"])[0]
    
    raw_parents = c.execute("""
        SELECT parent_id
        FROM category_to_parent
        WHERE child_id = ?;
        """, (id,),)
    category_data["parents"] = [parent[0] for parent in raw_parents]

    db.close()
    return render_template(
        "manageCategory_editor.html",
        category_nest=category_nest,
        category_data=category_data
    )
    
@category.route("/editCategory", methods=["POST"])
def editCategory():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        categoryToIdDict = {}
        headerToIdDict = {}
        for category in c.execute("SELECT name, id FROM category"):
            categoryToIdDict[category[0]] = category[1]

        for header in c.execute("SELECT name, id FROM category_header"):
            headerToIdDict[header[0]] = header[1]

        name = request.form.get("name")
        id = request.form.get("id")

        header = request.form.get("header")

        parent_list = request.form.getlist("parent")

        # delete in category, food_to categry, food to parent
        c.execute("DELETE FROM category WHERE id = ?", (id,),)
        c.execute("DELETE FROM category_to_parent WHERE child_id = ?", (id,),)

        c.execute(
            "INSERT INTO category (id, timestamp, name, category_header_id, user_id) VALUES (?, ?, ?, ?, ?)",
            (
                id, 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                name,
                headerToIdDict[header],
                hardCodeUserId,
            ),
        )

        category_id = c.lastrowid

        for parent in parent_list:
            c.execute(
                "INSERT INTO category_to_parent (parent_id, child_id) VALUES (?, ?)",
                (categoryToIdDict[parent], category_id),
            )

    db.commit()
    db.close
    return redirect("/")

@category.route("/manageCategory_editor_deactivate", methods=["POST"])
def manageCategory_editor_deactivate():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":
        c.execute("UPDATE category SET active = 0 WHERE id = ?", (request.form.get("id"),),)
        
    db.commit()
    db.close()

    # the page url will be /addFood which will cause route problems, so should do a redirect to index instead? yeap
    return redirect("/")