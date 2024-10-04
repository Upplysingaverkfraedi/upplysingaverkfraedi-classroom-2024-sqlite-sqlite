-- 1. Búa til töflu fyrir hlaup
CREATE TABLE IF NOT EXISTS hlaup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auðkenni hlaupsins
    upphaf DATETIME NOT NULL,              -- Tímasetning upphafs hlaups
    endir DATETIME NOT NULL,               -- Áætluð lok hlaups
    nafn TEXT NOT NULL,                    -- Nafn hlaupsins
    fjoldi INTEGER NOT NULL                -- Fjöldi þátttakenda
);

-- 2. Búa til töflu fyrir timataka
CREATE TABLE IF NOT EXISTS timataka (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auðkenni keppanda
    hlaup_id INTEGER NOT NULL,             -- Ytri lykill sem vísar í hlaup töfluna
    nafn TEXT NOT NULL,                    -- Nafn keppanda
    timi TEXT NOT NULL,                    -- Tími sem keppandi lauk hlaupinu á
    kyn TEXT,                              -- Kyn keppanda (ef gefið upp)
    aldur INTEGER,                         -- Aldur keppanda (ef gefið upp)
    UNIQUE(hlaup_id, nafn),                -- Kemur í veg fyrir tvítöku gagna
    FOREIGN KEY (hlaup_id) REFERENCES hlaup(id)
);

-- 3. Setja inn hlaup og keppendur (þú getur bætt við fleiri)
INSERT INTO hlaup (upphaf, endir, nafn, fjoldi)
VALUES ('2022-08-28 10:00:00', '2022-08-28 12:00:00', 'Íslandsót í criterium 2022', 1);

INSERT INTO timataka (hlaup_id, nafn, timi, kyn, aldur)
VALUES
(13, 'Jon Jonsson', '00:35:21', 'Karl', 25),
(13, 'Sara Sigurðardóttir', '00:40:15', 'Kona', 30),
(13, 'Arnar Arnalds', '00:29:05', 'Karl', 22);

-- 4. Sannreyna fjölda keppenda í hverju hlaupi
SELECT h.nafn AS hlaup, 
       h.fjoldi AS skradir_keppendur, 
       COUNT(t.id) AS raunverulegir_keppendur,
       CASE
           WHEN h.fjoldi = COUNT(t.id) THEN 'Passar'
           ELSE 'Passar ekki'
       END AS samanburdur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id;

-- 5. Athuga hvort einhver gögn séu tvítekin
SELECT nafn, COUNT(*) as fjoldi_tiltekinna_gagna
FROM timataka
GROUP BY hlaup_id, nafn, timi
HAVING COUNT(*) > 1;
