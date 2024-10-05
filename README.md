# Nauðsynleg forrit og uppsetning
Til að keyra verkefnið þarf eftirfarandi forrit:

- **SQLite**:
  - SQL er á flestum macOS tölvum og þarf því ekki að setja það upp.
  - Til að athuga hvort SQL er á tölvunni skrifið inn eftirfarandi í Terminal:
    ```sqlite3 --version``` 
  - Ef það þarf að setja upp SQLite, gerið það áður en hafist er handa við verkefnið. 
  - Einnig þarf að hlaða niður SQLite viðbótinni (finnið hana í 'extensions') í VS Code til að keyra SQL fyrirspurnir.

# Möppustrúktúr: 
## Liður 1: 
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
## Liður 2: 
```
data/
├─ isfolkid.db
create_isfolkid.sql
isfolkid.sql
README.md
```
## Liður 3: 
```
insert Data.py
createTables.sql
lidur3.py
Liður3.sql
```

# 1. Tíðni nafna á Íslandi 

## Lýsing verkefnis: 
Verkefnið felur í sér að sameina tíðnigögn úr tveimur CSV skrám, `first_names_freq.csv` og `middle_names_freq.csv`, í SQLite gagnagrunninn `names_freq.db`. Næst eftir að gögnin hafa verið sameinuð í töfluna (`names.sql`), er notuð SQL fyrirspurn til að greina vinsælasta nafn af hópmeðlinum, tíðni nafna hópmeðlima og segja til um hvenær nöfnin komu fyrst fram. 

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
    1. `realpath ` til að sjá hvar skráin er. Hjá mér það `cd /Users/elisabet/Documents/GitHub/sqlite-lannister`
    2. `sqlite3 names_freq.db`
    3. `.read names.sql`





# 2. Saga Ísfólksins

## Lýsing verkefnis: 
Verkefnið felur í sér að búa til skrár sem lýsa uppbyggingu gagnagrunns án gagna í skánni `create_isfolkid.sql`
og svara spurningum um persónur, tíðni og aðra mikilvæga þætti úr gagnagrunninum sem má finna í skránni `isfolkid.sql`. 
Nánari útskýring um `isfolkid.sql` má finna í md skránni ` utskyring_lidur2.md`.

## Allar skipanalínur sem þarf að keyra til að keyra lausnina ykkar
Skrifa í terminal...
```
sqlite3 data/isfolkid.db
.read isfolkid.sql
```
og 

```
sqlite3 data/create_isfolkid.db
.read create_isfolkid.sql
```

# 3. Gagnagrunnur fyrir tímataka.net

### Lýsing verkefnis
í þessu verkefni var haldið áfram að vinna með tímatöku-liðinn sem var kynntur í
[síðasta hópverkefni](https://github.com/Upplysingaverkfraedi/regex/?tab=readme-ov-file#4-gagna%C3%BArvinnsla).
Sannreyna átti með samsöfnun og hópun hvort fjöldi keppanda í `hlaup` töflunni væri réttur út frá
fjölda lína í `timataka` töflunni. 
Þar sem við erum hópur Lannister áttum við að skoða öll hlaup ágúst 2022 sem eru skráð inná timataka.net 
 
### SQLite3 gagnagrunnur

Gagnagrunnurinn hafði tvær töflur; `hlaup` sem má finna í skránni createTables.sql og `timataka` (sem er enn í vinnslu) sem tók saman upplýsingar um: 
    - `id`: Auðkenni
    - `upphaf`: Tímasetning hlaups (dagsetning og tími dags)
    - `endir`: Áætluð lok hlaups (dagsetning og tími dags)
    - `nafn`: Nafn hlaups
    - `fjoldi`: Fjöldi þátttakenda
    - og fleiri eftir þörfum.

`timataka.sql` sem býr til gagnagrunninn, les gögnin inn og sannreynir fjölda.

### Keyrsla
Skrifa neðantalið í terminal til að keyra:
`sqlite3 data.db < createTables.sql`
2. `python3 Lidur3.py`
3. `python3 insertData.py`

### RegEx útvíkkun
Allar segðir sem voru gerðar má finna í skránni lidur.py með hjálp frá síðunni Regex101.com
Þær lesa inn dagsetningar, linka og nafn, tölur, upphafstíma, lokatíma, fjölda þátttakenda, ár og mánuð. 
