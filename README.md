# 1. Tíðni nafna á Íslandi 

## Lýsing verkefnis: 
Verkefnið felur í sér að sameina tíðnigögn úr tveimur CSV skrám, `first_names_freq.csv` og `middle_names_freq.csv`, í SQLite gagnagrunninn `names_freq.db`. Næst eftir að gögnin hafa verið sameinuð í töfluna (`names.sql`), er notuð SQL fyrirspurn til að greina vinsælasta nafn af hópmeðlinum, tíðni nafna hópmeðlima og segja til um hvenær nöfnin komu fyrst fram. 


## Nauðsynleg forrit og uppsetning
Til að keyra verkefnið þarf eftirfarandi forrit:

- **SQLite**:
  - SQL er á flesum MAC tölvum er þarf því ekki að setja það upp.
  - Til að athuga hvort SQL er á tölvunni skrifið inn eftirfarandi í Terminal:
    ```sqlite3 --version``` 
  - Ef það þarf að setja upp SQLite, gerið það áður en hafist er handa við verkefnið. 
  - Einnig þarf að hlaða niður SQLite viðbótinni (finnið hana í 'extensions') í VS Code til að keyra SQL fyrirspurnir.


## Möppustrúktúr: 
```bash
├── names_freq.db
│   ├── first_names_freq.csv
│   ├── middle_names_freq.csv
├── names.sql
└── README.md
```

## Keyrsla á kóðanum: 
1. Opna Terminal 
2. Setja eftirfarandi í skipanalínu (ath. 1. lína breytist eftir tölvum)
    1. cd /Users/elisabet/Documents/GitHub/sqlite-lannister
    2. sqlite3 names_freq.db
    3. .read names.sql



