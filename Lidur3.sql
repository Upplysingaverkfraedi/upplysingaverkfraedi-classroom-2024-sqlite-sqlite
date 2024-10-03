-- Búa til töflu fyrir hlaup
CREATE TABLE IF NOT EXISTS hlaup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    upphaf DATETIME NOT NULL,  -- Tímasetning upphafs hlaups
    endir DATETIME,            -- Áætluð lok hlaups
    nafn TEXT NOT NULL,        -- Nafn hlaupsins
    fjoldi INTEGER             -- Fjöldi þátttakenda
);

-- Búa til töflu fyrir timataka
CREATE TABLE IF NOT EXISTS timataka (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hlaup_id INTEGER,          -- Ytri lykill sem vísar í hlaup töfluna
    nafn TEXT NOT NULL,        -- Nafn keppanda
    timi TEXT NOT NULL,        -- Tími sem keppandi lauk hlaupinu á
    kyn TEXT,                  -- Kyn keppanda (ef gefið upp)
    aldur INTEGER,             -- Aldur keppanda (ef gefið upp)
    UNIQUE(hlaup_id, nafn, timi),  -- Kemur í veg fyrir tvítöku gagna
    FOREIGN KEY (hlaup_id) REFERENCES hlaup(id)
);

-- Setja inn hlaup (dæmi fyrir Ljósanæturhlaup Lífsstíls)
INSERT INTO hlaup (upphaf, endir, nafn, fjoldi)
VALUES ('2022-08-31 18:00:00', '2022-08-31 20:00:00', 'Ljósanæturhlaup Lífsstíls', 200);

-- Setja inn keppendur fyrir Ljósanæturhlaup Lífsstíls
INSERT INTO timataka (hlaup_id, nafn, timi, kyn, aldur)
VALUES (1, 'Jon Jonsson', '00:35:21', 'Karl', 25);

INSERT INTO timataka (hlaup_id, nafn, timi, kyn, aldur)
VALUES (1, 'Sara Sigurðardóttir', '00:40:15', 'Kona', 30);

-- Bæta við fleiri hlaupagögnum ef þarf
-- Dæmi: Ofursprettþraut 3N
INSERT INTO hlaup (upphaf, endir, nafn, fjoldi)
VALUES ('2022-08-27 12:00:00', '2022-08-27 14:00:00', 'Ofursprettþraut 3N', 100);

-- Setja inn keppendur fyrir Ofursprettþraut 3N
INSERT INTO timataka (hlaup_id, nafn, timi, kyn, aldur)
VALUES (2, 'Arnar Arnalds', '00:29:05', 'Karl', 22);

-- Sannreyna fjölda keppenda í hverju hlaupi
SELECT h.nafn, h.fjoldi AS skradir_keppendur, COUNT(t.id) AS raunverulegir_keppendur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id;

-- Athuga hvort einhver gögn séu tvítekin (dæmi: sama nafn og tími í sama hlaupi)
SELECT nafn, COUNT(*) as fjoldi_tiltekinna_gagna
FROM timataka
GROUP BY hlaup_id, nafn, timi
HAVING COUNT(*) > 1;
