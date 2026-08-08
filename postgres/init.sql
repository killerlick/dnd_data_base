CREATE TABLE spells (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    source TEXT NOT NULL,
    type TEXT NOT NULL,
    casting_time TEXT NOT NULL,
    range TEXT NOT NULL,
    components TEXT NOT NULL,
    duration TEXT NOT NULL,
    description TEXT
);

CREATE TABLE Races (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE Classes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE ITEMS (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

create table characters (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    race_id INTEGER REFERENCES Races(id),
    class_id INTEGER REFERENCES Classes(id),
    level INTEGER NOT NULL
);

create table character_inventory (
    character_id INTEGER REFERENCES characters(id),
    item_id INTEGER REFERENCES ITEMS(id),
    quantity INTEGER NOT NULL,
    PRIMARY KEY (character_id, item_id)
);

create table character_spells (
    character_id INTEGER REFERENCES characters(id),
    spell_id INTEGER REFERENCES spells(id),
    PRIMARY KEY (character_id, spell_id)
);