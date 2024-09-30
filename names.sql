-- Búa til the name table ef hún er ekki þegar til
CREATE TABLE IF NOT EXISTS names (
    name TEXT NOT NULL,
    year INTEGER NOT NULL,
    frequency INTEGER NOT NULL,
    type TEXT NOT NULL,
    PRIMARY KEY (name, year, type)
);

--  Búa til temborary töflu frá cvs
CREATE TABLE IF NOT EXISTS temp (
    name TEXT NOT NULL,
    year INTEGER NOT NULL,
    frequency INTEGER NOT NULL
);

-- Setja eignafn skránna inn í nafna töfluna
.mode csv
.import data/first_names_freq.csv temp

--
INSERT INTO names (name, year, frequency, type)
SELECT name, year, frequency, 'first' FROM temp;

-- Hreinsa temp töfluna eftir fyrsta import
DELETE FROM temp;

-- Setja inn miðnöfna skrá gögnin inn í temp töfluna
.import data/middle_names_freq.csv temp

-- Setja miðnöfnin inn í nafnatöfluna
INSERT INTO names (name, year, frequency, type)
SELECT name, year, frequency, 'middle' FROM temp;

-- Drop temp töflunni
DROP TABLE IF EXISTS temp;

--Spurning 1, Hvaða nafn er vinsælast?
SELECT name, SUM(frequency) AS total_frequency
FROM names
WHERE name IN ('Snæfríður', 'Dalrós', 'Erlendur') AND type ="first"
GROUP BY name
ORDER BY total_frequency ASC
LIMIT 1;

--Spurning 2, hvenær voru nöfnin vinsælust?
SELECT name, year, MAX(frequency) AS max_frequency
FROM names
WHERE name IN ('Snæfríður', 'Dalrós', 'Erlendur')
GROUP BY name
ORDER BY name;

-- Spurning 3: Hvenær komu nöfnin fyrst fram
SELECT name, MIN(year) AS first_appearance
FROM names
WHERE name IN ('Snæfríður', 'Dalrós', 'Erlendur')
GROUP BY name
ORDER BY name;
