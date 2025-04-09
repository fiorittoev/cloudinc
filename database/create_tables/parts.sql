CREATE TABLE IF NOT EXISTS parts (
    part_id           VARCHAR(255) NOT NULL PRIMARY KEY, 
    part_name         TEXT NOT NULL,
    part_cost         FLOAT NOT NULL,
    part_manufacturer TEXT NOT NULL
);