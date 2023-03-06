import csv
import datetime
import json
import os

from bs4 import BeautifulSoup

FOLDER = "cronometer_html_pages"

cronometer_page_list = os.listdir(FOLDER)

ncdb_nutrient_list = []
with open("ncdb_nutrient_list.json") as json_file:
    ncdb_nutrient_list = json.load(json_file)

extraMsg = ""

currentTime_forFileNameONLY = datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")

with open(f"food_{currentTime_forFileNameONLY}.csv", mode="w") as food_csv:
    food_writer = csv.writer(
        food_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )

    food_writer.writerow(
        ["id", "timestamp", "user_id", "name", "description", "price", "active"]
    )

    with open(
        f"food_to_nutrient_{currentTime_forFileNameONLY}.csv", mode="w"
    ) as ftn_csv:
        ftn_writer = csv.writer(
            ftn_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        ftn_writer.writerow(["food_id", "nutrient_id", "quantity"])

        for csv_id, cronometer_page in enumerate(cronometer_page_list, start=16):
            food_writer.writerow(
                [
                    csv_id,
                    "2023-02-24 11:11:11",
                    0,
                    cronometer_page.replace(".html", ""),
                    "",
                    0,
                    1,
                ]
            )
            with open(f"{FOLDER}/" + cronometer_page, "r") as html_file:
                # with open("cronometer_html_pages/peanut.html", 'r') as html_file:
                content = html_file.read()
                soup = BeautifulSoup(content, "lxml")

                rows = soup.find_all("tr")

                crono_nutrient_list_for_debugging = []

                for row in rows:
                    if (
                        row.find("td").find("div")
                        and not row.find(class_="table-header")
                        and not row.find("td").find(class_="gwt-Label")
                        and row.find("td").find("div").text.strip() != ""
                    ):
                        name = row.find(class_="gwt-HTML").text.strip().lower()

                        crono_nutrient_list_for_debugging.append(name)

                        quantity_unit_dv = row.find_all(class_="gwt-Label")
                        raw_quantity = quantity_unit_dv[0].text.strip().replace("<", "")
                        if raw_quantity == "-":
                            extraMsg += f"{cronometer_page}---{name}--- quantity was '-' ncdb\n"
                            continue;
                        raw_quantity = float(raw_quantity)
                        unit = quantity_unit_dv[1].text.strip()
                        quantity = 0
                        if unit == "g":
                            quantity = raw_quantity
                        elif unit == "mg":
                            quantity = raw_quantity / 1000
                        elif unit == "Âµg":
                            quantity = raw_quantity / 1000000
                        elif unit == "kcal":
                            quantity = raw_quantity
                        elif unit == "IU":
                            quantity = raw_quantity * 2.5e-8
                        else:
                            extraMsg += f"{cronometer_page}---{name}---unknown unit\n"

                        ncdb_valid_count = 0

                        for ncdb_nutrient in ncdb_nutrient_list:
                            if name in [
                                name.lower().replace("_", " ")
                                for name in ncdb_nutrient["name_list"]
                            ]:
                                ftn_writer.writerow(
                                    [csv_id, ncdb_nutrient["id"], quantity]
                                )
                                ncdb_valid_count += 1

                        if ncdb_valid_count == 0:
                            extraMsg += f"{cronometer_page}---{name}---had no matches for ncdb\n"

                        if ncdb_valid_count > 1:
                            extraMsg += f"{cronometer_page}---{name}---had {ncdb_valid_count} matches for ncdb\n"

                # check if ncdb_nutrient_list in
                for ncdb_nutrient in ncdb_nutrient_list:
                    if not any(
                        [
                            name in crono_nutrient_list_for_debugging
                            for name in [
                                n.lower().replace("_", " ")
                                for n in ncdb_nutrient["name_list"]
                            ]
                        ]
                    ):
                        extraMsg += f"{cronometer_page}---had no ncdb_nutrient:{ncdb_nutrient['name_list'][0]} detected on the page\n"


with open(f"extraMsg_{currentTime_forFileNameONLY}.txt", "w") as f:
    f.write(extraMsg)

    # rows = soup.find_all('tr', class_="no-target")
    # for row in rows:
    #     cronometer_nutrient_list.append(row.find('div', class_="nutrient-name").text.strip())
    #     unit = row.find('td', class_="targets-table-unit").find('div').text

    # for cronometer_nutrient in cronometer_nutrient_list:
    #     includes_ignorecase = cronometer_nutrient.lower() in [ncdb_nutrient.lower().replace("_", " ") for ncdb_nutrient in ncdb_nutrient_name_list]
    #     if not (includes_ignorecase):
    #         print(cronometer_nutrient)
