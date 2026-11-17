-- Таблицы домашней коллекции. Даты хранятся как YYYY-MM-DD.
CREATE TABLE IF NOT EXISTS owners (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT
);
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, light TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS plants (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, species TEXT NOT NULL,
    interval_days INTEGER NOT NULL CHECK (interval_days > 0),
    last_watered TEXT NOT NULL,
    owner_id INTEGER REFERENCES owners(id),
    location_id INTEGER REFERENCES locations(id)
);
CREATE TABLE IF NOT EXISTS waterings (
    id INTEGER PRIMARY KEY,
    plant_id INTEGER NOT NULL REFERENCES plants(id),
    watered_on TEXT NOT NULL, note TEXT NOT NULL DEFAULT ''
);
