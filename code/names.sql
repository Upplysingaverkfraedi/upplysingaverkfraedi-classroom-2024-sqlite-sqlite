-- Output file
-- Búa til töflu til að geyma nafna fjöldann
CREATE TABLE IF NOT EXISTS names (
    name TEXT NOT NULL,
    year INTEGER NOT NULL,
    frequency INTEGER NOT NULL,
    type TEXT,
    PRIMARY KEY (name, year, type)
);

-- Setja gögnin í töflu
-- Merkja að ég sé að lesa inn gögn frá csv skrám
.mode csv 
-- importa gögnin
.import 'data\first_names_freq.csv' names
-- Setja öll gögn fyrir "first_name" sem first_names
UPDATE names SET type = 'first_name' WHERE type IS NULL; 

-- Gera það sama við seinni skránni nema middle_name
.import 'data\middle_names_freq.csv' names
UPDATE names SET type = 'middle_name' WHERE type IS NULL;

-- Output file sem texta skrá
.output names_output.txt

-- Svör á spurningum:

-- Spurning 1
-- Prenta út spurninguna 
SELECT 'Spurning 1: Hvaða hópmeðlimur á algengasta eiginnafnið??' AS question;
-- Setja niðurstöðurnar sem summa af öllu count eftir nöfnunum og prenta út hvaða nafn hefur flest count s.s. er alngengast
SELECT name, SUM(frequency) AS total_frequency
FROM names
-- Leita af eignarnöfnunum okkar þrem og prenta út svarið með fjöldanum af count fyrir það nafn sem er alngengast
WHERE type = 'first_name' AND name IN ('Þráinn', 'Ásdís', 'Gígja')
GROUP BY name
ORDER BY total_frequency DESC
LIMIT 1;

-- Spurning 2
-- Prenta út spurninguna
SELECT 'Spurning 2: Hvenær voru öll nöfnin vinsælust?' AS question;
-- Þessi kóði les bæði fyrstu og milli nöfnin okkar og skilar þeirri línu (row) sem hefur flest count s.s. hvenær hvert nafn var vinsælast
SELECT name, year
FROM (
    SELECT name, year, frequency,
    ROW_NUMBER() OVER (PARTITION BY name ORDER BY frequency DESC) AS row_num
    FROM names
    WHERE (type = 'first_name' AND name IN ('Ásdís', 'Gígja', 'Þráinn'))
    UNION ALL
    SELECT name, year, frequency,
    ROW_NUMBER() OVER (PARTITION BY name ORDER BY frequency DESC) AS row_num
    FROM names
    WHERE (type = 'middle_name' AND name IN ('Marín', 'Ágúst'))
) AS subquery
WHERE row_num = 1;

-- Spurning 3
-- Prenta út spurninguna
SELECT 'Spurning 3: Hvenær komu þau fyrst fram?' AS question;
-- Þessi kóði finnur minnsta árið sem er við hvert nafn og skilar svo nafninu með því ártali
SELECT name, MIN(year) AS first_appearance
FROM names
-- Hér er verið að segja hvar á að leita eftir hvaða nafni s.s. í hvaða skrá
WHERE (type = 'first_name' AND name IN ('Ásdís', 'Gígja', 'Þráinn'))
   OR (type = 'middle_name' AND name IN ('Marín', 'Ágúst'))
GROUP BY name
ORDER BY first_appearance;

-- Endurstilla output mode
.output stdout