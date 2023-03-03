import pprint
from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request, url_for

from scripts.helpers import *

# this is hardcoded for now
hardCodeUserId = 0


dri = Blueprint("dri", __name__, template_folder="templates")


@dri.route("/addDri", methods=["POST"])
def addDri():    
    db = get_db()
    c = db.cursor()
    
    nutrientDict_list = []
    for nutrient in c.execute("SELECT id, name FROM nutrient"):
        nutrientDict_list.append({"id":nutrient[0], "name":nutrient[1]})
    
    name = request.form.get("name")
    
    #verify that a row, with matching group_name and nutrient_id isn't inserted
    
    if not name:
        request.form.get("please provide a name for the DRI group")
    
    for nutrient in nutrientDict_list:
        c.execute("SELECT count(*) FROM dri WHERE group_name = ? AND nutrient_id = ? AND active = 1", (name, nutrient["id"]),)
        if c.fetchall()[0][0] > 0:
            return apology("DRI group name already in use")
        
        rda = request.form.get(f"rda_{nutrient['id']}")
        ul = request.form.get(f"ul_{nutrient['id']}")
        
        c.execute("""
        INSERT INTO dri (timestamp, group_name, nutrient_id, rda, ul, user_id)
        VALUES (?, ?, ?, ?, ?, ?);""",(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            nutrient["id"],
            rda,
            ul,
            hardCodeUserId
        ), )
    db.commit()
    db.close()
    return redirect("/")

@dri.route("/manageDri_searchResults")
def manageDri_searchResults():
    db = get_db()
    c = db.cursor()
        
    input = request.args.get("search")

    dri_results = {}

    raw_dri_results = ()
    if input:
        raw_dri_results = c.execute(
            """
            SELECT d.group_name, d.timestamp, u.name 
            FROM dri d
            JOIN user u
            ON d.user_id = u.id 
            WHERE d.active = 1
            AND d.group_name LIKE ?
            GROUP BY d.group_name;                           
            """,
            (f"%{input}%",),
        )
    else:
        raw_dri_results = c.execute(
            """
            SELECT d.group_name, d.timestamp, u.name 
            FROM dri d
            JOIN user u
            ON d.user_id = u.id 
            WHERE d.active = 1
            GROUP BY d.group_name;
            """
        )

    dri_results = listOfTuplesToListOfDict(
        raw_dri_results,
        ["name", "timestamp", "username"],
    )

    db.close()
    return render_template(
        "manageDri_searchResults.html", dri_results=dri_results
    )
    
@dri.route("/manageDriLoadEditor")
def manageDriLoadEditor():
    # load form inputs (beware loadFoodFormData will reopen and close the database), fixed by opening and closing the database outside the funciton
    db = get_db()
    c = db.cursor()


    foodFormData = loadFoodFormData(c)
    nutrient_nest = foodFormData["nutrient_nest"]
    
    group_name = request.args.get("name")

    for header in nutrient_nest:
        for nutrient in nutrient_nest[header]["list"]:
            
            info = c.execute("""
            SELECT rda, ul
            FROM dri
            WHERE active = 1
            AND group_name = ?
            AND nutrient_id = ?                      
            """,
            (group_name,
            nutrient["id"]),
            ).fetchall()
            
            if len(info) > 0:
                rda_and_ul = info[0]
                print(rda_and_ul)
                nutrient["rda"] = rda_and_ul[0]
                #use a shortcircuit to make 0 and alternative
                nutrient["ul"] = rda_and_ul[1]  

    db.close()
    return render_template("manageDri_editor.html", nutrient_nest=nutrient_nest, group_name=group_name)

@dri.route("/dri_editor_submit", methods=["POST"])
def manageFood_editor_submit():
    db = get_db()
    c = db.cursor()
    
    og_name = request.form.get("og_name")
    # name = request.form.get("name")
    
    if request.method == "POST":
        ## for now don't allow users to change the name
        # if og_name != name:
        #     c.execute("SELECT count(*) FROM dri WHERE group_name = ? AND active = 1", (name,))
        #     if c.fetchall()[0][0] > 0:
        #         return apology("DRI group name already in use")         
            
        c.execute("DELETE FROM dri WHERE group_name= ?", (og_name,),)
    
  
        
        nutrientDict_list = []
        for nutrient in c.execute("SELECT id, name FROM nutrient"):
            nutrientDict_list.append({"id":nutrient[0], "name":nutrient[1]})
        
        for nutrient in nutrientDict_list:
            
            rda = request.form.get(f"rda_{nutrient['id']}")
            ul = request.form.get(f"ul_{nutrient['id']}")
            
            c.execute("""
            INSERT INTO dri (timestamp, group_name, nutrient_id, rda, ul, user_id)
            VALUES (?, ?, ?, ?, ?, ?);""",(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                og_name,
                nutrient["id"],
                rda,
                ul,
                hardCodeUserId
            ), )
        
    db.commit()
    db.close()

    return redirect("/")