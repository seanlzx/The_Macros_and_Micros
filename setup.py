import sqlite3

conn = sqlite3.connect("nutrition.db")
c = conn.cursor()

# total fat, protein, carbs can calculate in frontend???? not important now maybe some other time
# nutrition grams and prices is all per 100 grams
# description, can keep details like antioxidants, antiinflamotries, bad stuff to like inflamatories, good bacteria/cultures, recommended timing, preparation tips, eating orange peels, etc
c.execute(
    """CREATE TABLE food (
            id INTERGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            description TEXT,
    """
    # Nutrients
    """calories REAL,"""
    # Carbs
    """carbohydrates REAL,"""
    # Cholestrol
    """cholestrol REAL"""
    # Proteins
    """proteins REAL,"""
    # Fats
    """
        total_fats REAL,
        monounsaturated_fats REAL,
        polyunsaturated_fats REAL,
        saturated_fats REAL,
        trans_fats REAL,  
        omega_3,"""
    # Vitamins
    """
        vitamin_a REAL,
        vitamin_b1 REAL,
        vitamin_b2 REAL,
        vitamin_b3 REAL,
        vitamin_b5 REAL,
        vitamin_b6 REAL,
        vitamin_b12 REAL,
        vitamin_D REAL,
        vitamin_E REAL,
        vitamin_k REAL,
        choline REAL,
        folic_acid REAL,
        """
    # Minerals
    """
        calcium REAL,
        chloride REAL,
        chromium REAL,
        copper REAL,
        fluoride REAL,
        iodine REAL
        iron REAL,
        magnesium REAL,
        manganese REAL,
        phosphorus REAL,
        potatssium REAL,
        selenium REAL,
        sodium REAL,
        sulfur REAL,
        zinc REAL,
        """
    # others
    """  
    fiber REAL,
    creatine REAL,
    caffeine REAL,
    """
    # harmful chemicals
    """
        mercury REAL,
        nitrates_and_nitrites REAL,
        Artificial_food_colors REAL
        )"""
)

c.execute(
    """
    CREATE UNIQUE INDEX idx_id ON food (id);
    """
)


# nutrition table should be able to derive antioxidants, antiinflamtories, etc
# also find a way to include anti inflamatory foods, select where contain anti inflmatory vitamins
c.execute(
    """
    CREATE TABLE nutrient (
        name TEXT PRIMARY KEY AUTOINCREMENT NOT NULL,
        timestamp TEXT NOT NULL,
        description TEXT,
        rda REAL
    )
    """
)

c.execute(
    """
    CREATE TABLE foodPrice (
        food_id INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        price REAL,
        FOREIGN KEY(food_id) REFERENCES food(id)
    )
    """
)

c.execute(
    """
    CREATE TABLE foodToCategory (
        food_id,
        category_id
    )
    """
)

c.execute(
    """
        CREATE TABLE category (
            category_id PRIMARY KEY AUTOINCREMENT NOT NULL,
            category_name
        )
    """
)

c.execute(
    """
        CREATE TABLE foodOrDishToList (
            food_id,
            dish_id,
            list_id NOT NULL
        )
    """
)

c.execute(
    """
        CREATE TABLE dish (
            food_id,
            dish_id,
        )
    """
)

c.execute(
    """
        CREATE TABLE list (
            list_id PRIMARY KEY AUTOINCREMENT NOT NULL,
            list_name
        )
    """
)

c.execute(
    """
        CREATE TABLE foodToMeal (
            meal_id 
            food_id
        )
    """
)

# create a way for user to create list of meals/foods, with quantities. example 'list of foods to take preworkout, postworkout, heavyday, lightday, cardioday, breakfast, lunch, supper,

conn.close()
