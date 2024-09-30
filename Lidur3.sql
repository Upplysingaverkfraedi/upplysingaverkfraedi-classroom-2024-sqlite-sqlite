-- Býr til töflu fyrir hlaup
CREATE TABLE IF NOT EXISTS hlaup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    upphaf DATETIME NOT NULL,
    endir DATETIME,
    nafn TEXT NOT NULL,
    fjoldi INTEGER
);

-- Býr til töflu fyrir timataka
CREATE TABLE IF NOT EXISTS timataka (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hlaup_id INTEGER,
    nafn TEXT NOT NULL,
    timi TEXT NOT NULL,
    kyn TEXT,
    aldur INTEGER,
    FOREIGN KEY (hlaup_id) REFERENCES hlaup(id)
);

-- Sannreynir fjölda keppenda í hverju hlaupi
SELECT h.nafn, COUNT(t.id) AS fjoldi_keppenda, h.fjoldi
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id;
