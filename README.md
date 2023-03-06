# The Macros and Micros | A CS50 Final Project

The Macros and Micros is a flask web app, to record user diets and track nutrition.

Set goals and limits (DRIs) for your nutritional needs. Input food details and meal details in a comprehensive and convenient way to keep track of your diet and nutrition.

The app has a footer below which should explain some of the terminologies and ideas of nutrition and how to use the app. The interface is covered in tooltips galore. Honestly I'm not sure if it might be an inundation of information, if I ever continue updating the app, I may release a full video tutorial.

The database in the project folder comes with example data for meals, foods, DRIs, nutrients and more.

[Final Project Video Demo](https://youtu.be/OpUSbIDQ5eg)

## Installation
- python is required
- pip install the libraries in the [requirements](requirements.txt) file
- Open your preferred terminal in the project folder `flask run`
- Open your preferred browser (I developed with Chrome but Edge should work), and enter the localhost URL into the address bar

## Create Food
Only name and price is required.

### Category Checkboxes
When you check a category, related categories are highlighted for you to check if desired, 
this is just to ease data use.

### Nutrient Inputs
All nutrients are stored as grams.

You may make use of the "mg" and "μg" converters.

## Manage Foods
Foods can be edited and deactivated through here.

When the search bar is left blank, all food data is loaded.

### Filters
Can filter by Categories, Combos, Nutrients.

Can filter by username.

Can filter by multiple keywords found in the description.

### Sort
Can order by last update, alphabetically, or price.

### Sort by nutrient
Can also order by a specified nutrient per dollar, per calorie, per gram.

Just choose a sort by nutrient option.

Input the desired nutrient (make sure the spelling is correct).

## Create Meal
Name and time required.

### Adding Food
Click "Add Food" to create a food input.

Iput the food input to search for food. (may use filters), press the x button to remove the food input.

### Adding Food via Combos
Search desired combo, and select it.

A combo ingredients can be added one by one.

All combo ingredients can be added with "Add All".

## Meal Records

![Image of meal records](https://i.imgur.com/daHRfsb.png)

### Sorting Meal Records.

Meal Records can be sorted from and to.

Click "newest" or "oldest" for sorting order.

### Meals 
are arranged under their dates.

Click the "edit" button to edit meals.

Foods and their quantities are lined underneath the title in grey boxes.

### Meal Nutritional Information
Nutritional Information for the meals can be expanded with the button underneath.

### Day Nutritional Information
The nutritional information for the day can be expanded with the button underneath the date.

## Creating Combos
Very similar to creating meals.

## Manage Combos
Can edit and deactivate combos through here.

## Creating Combos
Name and header is required.

The header is just for arrangement in the food form.

### Parent Categories
Parent categories for foods will be highlighted when the child category is checked in food forms.

## Manage Categories
Can edit and deactivate categories through here.

## Creating DRIs (Dietary Reference Intakes)
Name is required.

### RDAs (Recommended Dietary Allowance)
This is the amount you desire to reach for the nutrient.

### ULs (Upper Limit)
This is the amount you should limit yourself to for the nutrient.

## Managing DRIs
As of now you can only edit the RDAs and ULs for RDAs.

Names cannot be edited (will be resolved in a future update).

DRIs cannot be deactivated (will be resolved in a future update).

## Settings
currently name, weight, height, gender, age does not mean anything. 
In future updates a default DRI will be selected and configured to the weight, gender, age of user.

### Configure startup sorting of meals
"from" and "to" dates can be customize here.

## Other Tools
I have a few tools included in [/docs and devtools](docs%20and%20devtools)

setup.py initialises a new database with data from [/docs and devtools/initial_data](/docs%20and%20devtools/initial_data)

### getting data from various sources

[./Extracting USDA database](docs%20and%20devtools/Tools%20for%20extracting%20food%20data) contains a bunch of tools i used to extract/ scrape data from various sources. I kind of hacked my way through making these tools for personal/developmental use though, so their pretty unituitive to use, if I ever continue this project, I'll consider making a better way to extract food data from various sources, or even integrating the tool within the web app itself.

To use [cronometer_scraper.py](docs%20and%20devtools/Tools%20for%20extracting%20food%20data/cronometer_scraper.py), you'll have to manually save the cronometer html page into the the [cronometer_html_pages]("docs and devtools/Tools for extracting food data/cronometer_html_pages") folder.

Once you run [cronometer_scraper.py](docs%20and%20devtools/Tools%20for%20extracting%20food%20data/cronometer_scraper.py) it will produce a "\<insert current time\> food.csv" and a "\<insert current time\>  food_to_nutrient.csv" file, the columns from the newly created files can be transferred into the ends of the corresponding file within initial_data folder.

When you run setup.py a "\<insert current time\> nutrient.db" file should be created, just rename the file "nutrient.db" and replace the "nutrient.db" in the main folder

There is also a tool to [extract from the USDA database](docs%20and%20devtools/Tools%20for%20extracting%20food%20data/legacy%20files/extract_usda_components.py), however it's currently incomplete and even then, would require a USDA API key.




