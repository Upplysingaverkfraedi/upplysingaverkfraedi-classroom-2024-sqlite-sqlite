-- Liður 1

CREATE TABLE IF NOT EXISTS names (
    name varchar(20),
    year int,
    frequency int,
    type text
);

CREATE TABLE IF NOT EXISTS temp_table (
    name varchar(20),
    year int,
    frequency int
);

.mode csv
.import data/first_names_freq.csv temp_table
INSERT INTO names(name, year, frequency, type) SELECT name, year, frequency, "eiginnafn" FROM temp_table;
DELETE FROM temp_table;


.import data/middle_names_freq.csv temp_table
INSERT INTO names(name, year, frequency, type) SELECT name, year, frequency, "millinafn" FROM temp_table;
DROP TABLE temp_table;

-- Liður 2

-- a. Hvaða hópmeðlimur á algengasta eiginnafnið?
SELECT name, SUM(frequency) AS total_frequency
FROM names
WHERE name IN ('Elísabet', 'Alda', 'Benedikt') AND type="eiginnafn"
GROUP BY name
ORDER BY total_frequency DESC
LIMIT 1;

-- Elísabet er algengasta nafnið. 


-- b. Hvenær voru öll nöfnin vinsælust?
SELECT name, year, MAX(frequency) AS highest_frequency
FROM names
WHERE name IN ('Elísabet', 'Alda', 'Benedikt') AND type="eiginnafn"
GROUP BY name 
ORDER BY name, highest_frequency DESC;

-- Alda var vinsælast 1963, Benedikt árið 1996 og Elísabet árið 1979. 


-- c. Hvenær komu þau fyrst fram? 
SELECT name, MIN(year) AS first_appearance
FROM names
WHERE name IN ('Elísabet', 'Alda', 'Benedikt')
GROUP BY name
ORDER BY first_appearance;

-- Benedikt kom fyrst fram 1904, Elísabet 1905 og Alda 1916. 