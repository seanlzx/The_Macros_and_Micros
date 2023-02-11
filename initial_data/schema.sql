CREATE TABLE food (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price REAL,
    active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE sqlite_sequence(name, seq);
CREATE UNIQUE INDEX food_idx_id ON food (id);

CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp TEXT NOT NULL,
    name TEXT NOT NULL,
    category_header_id INTEGER NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (category_header_id) REFERENCES category_header(id)
);

CREATE TABLE food_to_category (
    food_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (food_id) REFERENCES food(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE INDEX food_to_category_idx_food_id ON food_to_category (food_id);
CREATE INDEX food_to_category_idx_category_id ON food_to_category (category_id);

CREATE TABLE category_to_parent (
    parent_id INTEGER NOT NULL,
    child_id INTEGER NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES category(id),
    FOREIGN KEY (child_id) REFERENCES category(id)
);

CREATE TABLE category_header (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE nutrient (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    nutrient_header_id INTEGER NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (nutrient_header_id) REFERENCES nutrient_header(id)
);

CREATE TABLE nutrient_header (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
);

-- Dietary Reference Intakes (DRIs) name refers to the DRI group (infants, children, males, females, pregnancy, lactation of various ages)
-- null for rda and ul means not determined
CREATE TABLE dri (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp TEXT NOT NULL,
    group_name TEXT NOT NULL,
    nutrient_id INTEGER NOT NULL,
    rda REAL,
    ul REAL,
    active INTEGER NOT NULL DEFAULT 1,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (nutrient_id) REFERENCES nutrient(id)
);

--if quantity 0 than take it as unknown
CREATE TABLE food_to_nutrient (
    food_id INTEGER NOT NULL,
    nutrient_id INTEGER NOT NULL,
    quantity REAL,
    FOREIGN KEY (food_id) REFERENCES food(id),
    FOREIGN KEY (nutrient_id) REFERENCES nutrient(id)
);

CREATE INDEX food_to_nutrient_idx_food_id ON food_to_nutrient (food_id);
CREATE INDEX food_to_nutrient_idx_nutrient_id ON food_to_nutrient (nutrient_id);
CREATE INDEX food_to_nutrient_idx_quantity ON food_to_nutrient (quantity);

CREATE TABLE combo (
    id INTEGER PRIMARY KEY NOT NULL,
    timestamp TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE INDEX combo_idx_timestamp ON combo (timestamp);
CREATE INDEX combo_idx_name ON combo (name);

--if quantity 0, than take it as unknown
CREATE TABLE combo_to_food (
    combo_id INTEGER NOT NULL,
    food_id INTEGER NOT NULL,
    quantity INTEGER,
    FOREIGN KEY (combo_id) REFERENCES combo(id),
    FOREIGN KEY (food_id) REFERENCES food(id)
);

CREATE TABLE IF NOT EXISTS meal (
    id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    name TEXT,
    description TEXT,
    time_of_meal TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE meal_to_food (
    meal_id INTEGER NOT NULL,
    food_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    FOREIGN KEY (meal_id) REFERENCES meal(id),
    FOREIGN KEY (food_id) REFERENCES food(id)
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    weight real NOT NULL,
    height real NOT NULL,
    gender TEXT NOT NULL,
    age INTEGER NOT NULL,
    user_type INTEGER NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);
