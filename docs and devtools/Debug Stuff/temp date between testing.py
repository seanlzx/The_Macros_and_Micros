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
    
    raw_meals = c.execute("""
        SELECT id, name, description, time_of_meal FROM meal 
        WHERE active=1 AND user_id = 0 AND time_of_meal BETWEEN "2023-02-01 00:01:01" AND "2023-02-23 01:01:00" ORDER BY time_of_meal""",
    )
    
    for meal in raw_meals:
        print(meal)
    
    # sqliteConnection.commit()
except sqlite3.Error as error:
    print(error)
    
finally:
    if sqliteConnection:
        sqliteConnection.close()
