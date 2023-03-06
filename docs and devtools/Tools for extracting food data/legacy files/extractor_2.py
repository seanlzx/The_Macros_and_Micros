import json

import requests

# nutri calc database nutrient list
ncdb_nutrient_list = [
    {"id": 0, "name_list": ["calories", "Energy"]},
    {
        "id": 1,
        "name_list": [
            "carbohydrates",
            "Carbohydrate, by difference",
            "Carbohydrate, by summation",
        ],
    },
    {"id": 2, "name_list": ["fiber", "Fiber, total dietary", "Total dietary fiber"]},
    {"id": 3, "name_list": ["proteins", "Protein"]},
    {"id": 4, "name_list": ["cholestrol", "Cholesterol"]},
    {"id": 5, "name_list": ["total_fats", "Total lipid (fat)", "Total fat (NLEA)"]},
    {
        "id": 6,
        "name_list": ["monounsaturated_fats", "Fatty acids, total monounsaturated"],
    },
    {
        "id": 7,
        "name_list": ["polyunsaturated_fats", "Fatty acids, total polyunsaturated"],
    },
    {"id": 8, "name_list": ["saturated_fats", "Fatty acids, total saturated"]},
    {"id": 9, "name_list": ["trans_fats","Fatty acids, total trans"]},
    {"id": 10, "name_list": ["omega_3"]},
    {"id": 11, "name_list": ["vitamin_A", "Vitamin A, RAE"]},
    {"id": 12, "name_list": ["vitamin_B1", "Thiamin"]},
    {"id": 13, "name_list": ["vitamin_B2", "Riboflavin"]},
    {"id": 14, "name_list": ["vitamin_B3", "Niacin"]},
    {"id": 15, "name_list": ["vitamin_B5", "Pantothenic acid"]},
    {"id": 16, "name_list": ["vitamin_B6", "Vitamin B-6"]},
    {"id": 17, "name_list": ["vitamin_B12", "Vitamin B-12"]},
    {"id": 18, "name_list": ["vitamin_C", "Vitamin C, total ascorbic acid"]},
    {"id": 19, "name_list": ["vitamin_D", "Vitamin D (D2 + D3), International Units"]},
    {"id": 20, "name_list": ["vitamin_E", "Vitamin E (alpha-tocopherol)", "Vitamin E"]},
    {"id": 21, "name_list": ["vitamin_k", "Vitamin K (phylloquinone)"]},
    {"id": 22, "name_list": ["choline", "Choline, total"]},
    {"id": 23, "name_list": ["folate", "Folate, total"]},
    {"id": 24, "name_list": ["calcium", "Calcium, Ca"]},
    {"id": 25, "name_list": ["chloride", "Chlorine, Cl"]},
    {"id": 26, "name_list": ["chromium","Chromium, Cr"]},
    {"id": 27, "name_list": ["copper", "Copper, Cu"]},
    {"id": 28, "name_list": ["fluoride", "Fluoride, F"]},
    {"id": 29, "name_list": ["iodine", "Iodine, I"]},
    {"id": 30, "name_list": ["iron", "Iron, Fe"]},
    {"id": 31, "name_list": ["magnesium", "Magnesium, Mg"]},
    {"id": 32, "name_list": ["manganese", "Manganese, Mn"]},
    {"id": 33, "name_list": ["phosphorus", "Phosphorus, P"]},
    {"id": 34, "name_list": ["potatssium", "Potassium, K"]},
    {"id": 35, "name_list": ["selenium", "Selenium, Se"]},
    {"id": 36, "name_list": ["sodium", "Sodium, Na"]},
    {"id": 37, "name_list": ["sulfur", "Sulfur, S"]},
    {"id": 38, "name_list": ["zinc", "Zinc, Zn"]},
    {"id": 39, "name_list": ["creatine"]},
    {"id": 40, "name_list": ["caffeine", "Caffeine"]},
    {"id": 41, "name_list": ["good_bacteria"]},
    {"id": 42, "name_list": ["mercury"]},
    {"id": 43, "name_list": ["nitrates_and_nitrites"]},
    {"id": 44, "name_list": ["artificial_food_colors"]},
    {"id": 45, "name_list": ["vitamin_B7","biotin"]},
    {"id": 46, "name_list": ["molybdenum", "Molybdenum, Mo"]},
    {"id": 47, "name_list": ["linoleic_acid"]},
    {"id": 48, "name_list": ["a-linolenic_acid"]},
    {"id": 49, "name_list": ["nickel", "Nickel, Ni"]},
    {"id": 50, "name_list": ["boron", "Boron, B"]},
    {"id": 51, "name_list": ["arsenic"]},
    {"id": 52, "name_list": ["chromium"]},
    {"id": 53, "name_list": ["silicon"]},
    {"id": 54, "name_list": ["sulfate"]},
    {"id": 55, "name_list": ["vanadium"]},
    {"id": 56, "name_list": ["total_sugar", "Sugars, total including NLEA", "Sugars, Total"]},
    {"id": 57, "name_list": ["glucose"]},
    {"id": 58, "name_list": ["fructose"]},
    {"id": 59, "name_list": ["sucrose"]},
    {"id": 60, "name_list": ["alcohol", "Alcohol, ethyl"]},
]

    

fdc_id_list = [
    # peanuts, dry roasted, salted
    2342994,
    # Egg, whole, boiled or poached
    2342629,
    # Spices, turmeric, ground172231
    172231,
    #fuji apples, fuji
    2246655,
]

json_text = requests.get(
    f"https://api.nal.usda.gov/fdc/v1/food/2342994?api_key=<lolololololololol>"
).text
_dict = json.loads(json_text)

print(_dict["inputFoods"][0]["amount"])
print(_dict["inputFoods"][0]["unit"])
print(_dict["description"])
for nutrient in _dict["foodNutrients"]:
    print("-------------------------------------------")
    print(nutrient["nutrient"]["name"])
    print(nutrient["amount"])
    print(nutrient["nutrient"]["unitName"])

# rmemeber to make sure the nutrient matching is not case sensitive

# remember for some reason the USDA does not record omega 3
