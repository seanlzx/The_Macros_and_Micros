import os
import sqlite3
from datetime import datetime
from sqlite3 import OperationalError

import pandas as pd

# if nutrition.db doesn't exist, it's created implicitly
conn = sqlite3.connect(f"nutrition.db")
c = conn.cursor()

file = open(f"initial_data/schema.sql", 'r')
sqlSchemaText = file.read()
file.close()

sqlCommandList = sqlSchemaText.split(';')

for command in sqlCommandList:
    try:
        c.execute(command)
    except OperationalError as msg:
        print('Commands skipped:', msg)
        


# must be updated whenever a new initial_data csv is created
# OMIT the .csv at the end
table_list = [file_string.replace(".csv", "") for file_string in list(filter(lambda file_string: ".csv" in file_string, os.listdir("initial_data")))]

for table in table_list:
    data = pd.read_csv(f'initial_data/{table}.csv')
    data.to_sql(table, conn, if_exists='append', index=False)
    
conn.close();

        
