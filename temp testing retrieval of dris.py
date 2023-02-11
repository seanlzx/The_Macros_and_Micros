import sqlite3
from datetime import datetime
# pprint just to print things nicely
from pprint import pprint

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
    sqliteConnection = sqlite3.connect("nutrition.db")
    c = sqliteConnection.cursor()
    
    nutrient_headers = listOfTuplesToListOfDict(c.execute("SELECT id, name FROM nutrient_header;"), ["id", "name"])
    
    for header in nutrient_headers:
        raw_dri_list = c.execute("""
        SELECT n.id AS nutrient_id, n.name AS name, d.rda AS rda, d.ul AS ul
        FROM nutrient n
        JOIN dri d
        ON n.id = d.nutrient_id
        WHERE n.nutrient_header_id = ?
        AND d.active = 1 AND n.active = 1
        AND d.group_name = ?;
        """, (header["id"], hardCodeDriGroupName))
        header["nutrients"] = listOfTuplesToListOfDict(raw_dri_list, ["nutrient_id", "name", "rda", "ul"])
    
    pprint(nutrient_headers)
except sqlite3.Error as error:
    print(error)
    
finally:
    if sqliteConnection:
        sqliteConnection.close()
