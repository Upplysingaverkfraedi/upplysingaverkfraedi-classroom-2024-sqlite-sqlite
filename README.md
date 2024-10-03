# 1. Tíðni nafna á Íslandi 

## Lýsing verkefnis: 
Verkefnið felur í sér að sameina tíðnigögn úr tveimur CSV skrám, `first_names_freq.csv` og `middle_names_freq.csv`, í SQLite gagnagrunninn `names_freq.db`. Næst eftir að gögnin hafa verið sameinuð í töfluna (`names.sql`), er notuð SQL fyrirspurn til að greina vinsælasta nafn af hópmeðlinum, tíðni nafna hópmeðlima og segja til um hvenær nöfnin komu fyrst fram. 


## Nauðsynleg forrit og uppsetning
Til að keyra verkefnið þarf eftirfarandi forrit:

- **SQLite**:
  - SQL er á flestum macOS tölvum og þarf því ekki að setja það upp.
  - Til að athuga hvort SQL er á tölvunni skrifið inn eftirfarandi í Terminal:
    ```sqlite3 --version``` 
  - Ef það þarf að setja upp SQLite, gerið það áður en hafist er handa við verkefnið. 
  - Einnig þarf að hlaða niður SQLite viðbótinni (finnið hana í 'extensions') í VS Code til að keyra SQL fyrirspurnir.

## Búa til gagnasafnið `names_freq.db`: 
Við þurfum að byrja á því að sameina gögnin okkar í eitt gagnasafn. 
1. Opna Terminal 
2. Setja path fyrir hvert þú vilt fá skránna
    1. Hjá mér er það: `cd/Documents/GitHub/sqlite-lannister`
3. Búa til gagnasafnið og töfluna: `sqlite3 names_freq.db < names.sql`
4. Athuga hvort það sé komið: `sqlite3 names_freq.db`
5. Ef þú vilt sjá töfluna: `.tables`


## Keyrsla á kóðanum: 
1. Opna Terminal 
2. Setja eftirfarandi í skipanalínu (ath. 1. lína breytist eftir tölvum)
    1. `cd /Users/elisabet/Documents/GitHub/sqlite-lannister`
    2. `sqlite3 names_freq.db`
    3. `.read names.sql`



## Möppustrúktúr: 
```bash
/sqlite-lannister
├── data/
     input/ 
         ├── first_names_freq.csv
         └── middle_names_freq.csv
      output/
         ├── names_freq.db
├── code/
     ├── names.sql
└── README.md
```
