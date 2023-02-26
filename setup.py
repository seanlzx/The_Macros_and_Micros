import sqlite3
from sqlite3 import OperationalError

import pandas as pd

# if nutrition.db doesn't exist, it's created implicitly
conn = sqlite3.connect("nutrition.db")
c = conn.cursor()

file = open('initial_data/schema.sql', 'r')
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
table_list = [
    'category_header',
    'category_to_parent',
    'category',
    'dri',
    'nutrient_header',
    'nutrient',
    'food',
    'food_to_nutrient',
    'user'
]

for table in table_list:
    data = pd.read_csv(f'initial_data/{table}.csv')
    data.to_sql(table, conn, if_exists='append', index=False)
    
conn.close();

        
