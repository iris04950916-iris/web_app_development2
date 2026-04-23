CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    image_url VARCHAR(255),
    calories FLOAT,
    protein FLOAT,
    carbs FLOAT,
    fat FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recipe_category (
    recipe_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id, category_id),
    FOREIGN KEY(recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
    FOREIGN KEY(category_id) REFERENCES categories (id) ON DELETE CASCADE
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    amount VARCHAR(50) NOT NULL,
    FOREIGN KEY(recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
);

CREATE TABLE steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    FOREIGN KEY(recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
);
