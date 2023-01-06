import sqlite3
from os import path
from pathlib import Path

from flask import g, request

parent = Path(path.dirname(path.abspath(__file__))).parent.absolute()
DATABASE = path.join(parent,"nutrition.db")

print(DATABASE)

def getFormListValues(list):
    dict = {}
    for str in list:
        value = request.form.get(str)
        if value:
            dict[str] = value

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
        
