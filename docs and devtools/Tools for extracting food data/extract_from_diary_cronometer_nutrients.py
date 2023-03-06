import json
import pprint

from bs4 import BeautifulSoup

with open('Oatmeal Quick Cooking.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml')

    cronometer_nutrient_list = []

    rows = soup.find_all('tr')
    for row in rows:
        if row.find('td').find('div') and not row.find(class_="table-header") and not row.find('td').find(class_="gwt-Label") and row.find('td').find('div').text.strip() != "" :
            cronometer_nutrient_list.append(row.find('td').find('div').text.strip())
        
    with open('ncdb_nutrient_list.json') as json_file:
        ncdb_nutrient_list = json.load(json_file)
        
        ncdb_nutrient_name_list = []

        for ncdb_nutrient in ncdb_nutrient_list:
            ncdb_nutrient_name_list.extend(ncdb_nutrient["name_list"])

        count = 0
        for cronometer_nutrient in cronometer_nutrient_list:
            includes_ignorecase = cronometer_nutrient.lower() in [ncdb_nutrient.lower().replace("_", " ") for ncdb_nutrient in ncdb_nutrient_name_list]
            if not (includes_ignorecase):
                print(cronometer_nutrient)
                count += 1
                
        print("count: ", count)