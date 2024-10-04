# 3. Gagnagrunnur fyrir tímataka.net

### Lýsing verkefnis
í þessu verkefni var haldið áfram að vinna með tímatöku-liðinn sem var kynntur í
[síðasta hópverkefni](https://github.com/Upplysingaverkfraedi/regex/?tab=readme-ov-file#4-gagna%C3%BArvinnsla).
Sannreyna átti með samsöfnun og hópun hvort fjöldi keppanda í `hlaup` töflunni væri réttur út frá
fjölda lína í `timataka` töflunni. 
Þar sem við erum hópur Lannister áttum við að skoða öll hlaup ágúst 2022 sem eru skráð inná timataka.net 
 
### Möppustrúktur 
insert Data.py
createTables.sql
lidur3.py
Liður3.sql

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
