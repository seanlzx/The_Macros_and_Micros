import sqlite3
from os import path
from pathlib import Path

from flask import g, render_template, request

hardCodeUserId = 0
hardCodeDriGroupName = "male 19-30"

parent = Path(path.dirname(path.abspath(__file__))).parent.absolute()
DATABASE = path.join(parent,"nutrition.db")

def getFormListValues(list):
    dict = {}
    for str in list:
        value = request.form.get(str)
        if value:
            dict[str] = value
        else:
            dict[str] = ""

    return dict

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# ensure the the number of elements in tuple is equal to elements in listOfKey
def listOfTuplesToListOfDict(listOfTuples, listOfKeys):
    list = []
    for tuple in listOfTuples:
        list.append(tupleToDict(tuple, listOfKeys))
    return list
        
def apology(message):
    return render_template("apology.html", message=message)
        
def tupleToDict(tuple, listOfKeys):
    dict = {}
    for key, item in zip(listOfKeys, tuple):
        dict[key] = item
    return dict

# this is a stupider function to help the below function
def keys_and_dict_to_dict(keys, dict):
    new_dict = {}
    for key in keys:
        new_dict[key] =  dict[key]
    return new_dict

# this is a stupid function, takes a header dict relation to another dictionary and returns a nesting rearrangement
def header_nesting(header_dict_list, child_dict_list, keys):
    nest = {}
    for header_dict_list in header_dict_list:
        nest[header_dict_list["id"]] = {"name": header_dict_list["name"], "list": []}

    for child_dict in child_dict_list:
        nest[child_dict["header_id"]]["list"].append(
            keys_and_dict_to_dict(keys, child_dict)
        )
    return nest    
        
def loadFoodFormData(c):
    dict = {}
    
    # produce category_hierarchy
    raw_header_list = c.execute("SELECT id, name FROM category_header")
    header_dict_list = listOfTuplesToListOfDict(raw_header_list, ["id", "name"])

    raw_header_category_join_list = c.execute(
        """
            SELECT ch.id AS header_id, c.id AS category_id, c.name AS category
            FROM category c
            JOIN category_header ch
            ON c.category_header_id = ch.id
            ORDER BY c.timestamp, c.id;
        """
    )
    header_category_join_dict_list = listOfTuplesToListOfDict(
        raw_header_category_join_list, ["header_id", "id", "name"]
    )

    dict["category_nest"] = header_nesting(
        header_dict_list, header_category_join_dict_list, ["id", "name"]
    )

    # produce nutrient_hierarchy
    raw_header_list = c.execute("SELECT id, name FROM nutrient_header")
    header_dict_list = listOfTuplesToListOfDict(raw_header_list, ["id", "name"])

    raw_header_nutrient_dri_join_list = c.execute(
        """
            SELECT nh.id AS header_id, n.id AS id, n.name AS name, n.description AS description, 
            dri.group_name AS group_name, dri.rda AS rda, dri.ul AS ul
            FROM nutrient n
            JOIN nutrient_header nh
            ON n.nutrient_header_id = nh. id
            JOIN dri
            ON n.id = dri.nutrient_id
			WHERE dri.group_name = ?
            ORDER BY n.timestamp, n.id; 
            """,
        (hardCodeDriGroupName,),
    )

    header_nutrient_dri_join_dict_list = listOfTuplesToListOfDict(
        raw_header_nutrient_dri_join_list,
        ["header_id", "id", "name", "description", "group_name", "rda", "ul"],
    )

    dict["nutrient_nest"] = header_nesting(
        header_dict_list,
        header_nutrient_dri_join_dict_list,
        ["id", "name", "description", "group_name", "rda", "ul"],
    )
    
    return dict

