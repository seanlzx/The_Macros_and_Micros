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
    sqliteConnection = sqlite3.connect("nutrition.db")
    c = sqliteConnection.cursor()
    
    rows_raw = c.execute("SELECT id, timestamp FROM nutrient")

    rows = listOfTuplesToListOfDict(rows_raw, ["id", "timestamp"])
    
    for row in rows:
        t = row["timestamp"].split(" ")
        t = t[0].split("/") + t[1].split(":")
        t = f"{t[0]}-{t[1]}-{t[2]} {t[3]}:{t[4]}:{t[5]}"
        c.execute("UPDATE nutrient SET timestamp = ? WHERE id = ?", (t, row["id"]))
    
    sqliteConnection.commit()
except sqlite3.Error as error:
    print(error)
    
finally:
    if sqliteConnection:
        sqliteConnection.close()
