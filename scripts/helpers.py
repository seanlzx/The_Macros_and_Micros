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