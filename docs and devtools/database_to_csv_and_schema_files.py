import os
import sqlite3
from datetime import datetime
from sqlite3 import OperationalError

import pandas as pd

# if nutrition.db doesn't exist, it's created implicitly
conn = sqlite3.connect("nutrition.db")
c = conn.cursor()

file = open("initial_data/schema.sql", 'r')
file.close()

currentTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

# must be updated whenever a new initial_data csv is created
# OMIT the .csv at the end
table_list = [file_string.replace(".csv", "") for file_string in list(filter(lambda file_string: ".csv" in file_string, os.listdir("initial_data")))]

c.execute(".headers on")
c.execute(".mode csv")

for table in table_list:
    try:
        c.execute(f".output {currentTime}_initial_data/{table}.csv")
        c.execute(f"SELECT * FROM {table}")
    except OperationalError as msg:
        print('Commands skipped:', msg)
    
conn.close();
