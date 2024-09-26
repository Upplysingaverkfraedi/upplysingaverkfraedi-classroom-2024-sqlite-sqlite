-- Output file
-- Create the table for storing name frequencies
CREATE TABLE IF NOT EXISTS names (
    name TEXT NOT NULL,
    year INTEGER NOT NULL,
    frequency INTEGER NOT NULL,
    type TEXT,
    PRIMARY KEY (name, year, type)
);

-- Load data into the table
.mode csv
.import 'data\first_names_freq.csv' names
UPDATE names SET type = 'first_name' WHERE type IS NULL;

.import 'data\middle_names_freq.csv' names
UPDATE names SET type = 'middle_name' WHERE type IS NULL;

-- Output file
.output names_output.txt

-- Analysis Queries:

-- Spurning 1
SELECT 'Spurning 1: Hvaða hópmeðlimur á algengasta eiginnafnið??' AS question;
SELECT name, MAX(frequency) AS max_frequency
FROM names
WHERE type = 'first_name' AND name IN ('Þráinn', 'Ásdís', 'Gígja')
GROUP BY name
ORDER BY max_frequency DESC
LIMIT 1;

-- Spurning 2
SELECT 'Spurning 2: Hvenær voru öll nöfnin vinsælust?' AS question;
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
SELECT 'Spurning 3: Hvenær komu þau fyrst fram?' AS question;
SELECT name, MIN(year) AS first_appearance
FROM names
WHERE (type = 'first_name' AND name IN ('Ásdís', 'Gígja', 'Þráinn'))
   OR (type = 'middle_name' AND name IN ('Marín', 'Ágúst'))
GROUP BY name
ORDER BY first_appearance;

-- Reset output mode
.output stdout