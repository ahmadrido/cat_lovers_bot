CREATE TABLE cat_knowledge (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    category VARCHAR(50),
    embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cat_breeds (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    description TEXT,
    origin VARCHAR(50),
    temperament TEXT
);

CREATE TABLE cat_diseases (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    symptoms TEXT,
    treatment_suggestion TEXT,
    danger_level TEXT
);
