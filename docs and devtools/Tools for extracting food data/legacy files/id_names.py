import pprint
import sqlite3
from datetime import datetime


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
    sqliteConnection = sqlite3.connect("../nutrition.db")
    c = sqliteConnection.cursor()
    
    raw_nutrients = c.execute("SELECT id, name FROM nutrient")
    
    nutrient_list = []
    for _tuple in raw_nutrients:
        _dict = {}
        _dict["id"] = _tuple[0]
        _dict["name_list"] = []
        _dict["name_list"].append(_tuple[1])
        nutrient_list.append(_dict)
        
    pprint.pprint(nutrient_list)
except sqlite3.Error as error:
    print(error)
    
finally:
    if sqliteConnection:
        sqliteConnection.close()
