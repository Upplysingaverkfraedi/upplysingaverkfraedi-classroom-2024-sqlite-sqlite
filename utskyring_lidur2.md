## Hér að neðan eru nánari útskýringar um skránna isfolkid.sql

#### Hversu margar aðalpersónur eru í bókabálkinum?

Í skránni má sjá tiltölulega flókna forritun en í stuttu máli er tekið streng úr dálkinum *characters* í töflunni *books*, skipt honum í undirstrengi með því að nota kommur sem skilgreinda skiptanalínu og telur síðan fjölda mismunandi strengja.

#### Hversu margar persónur eru í hverri bók?

Byrjar á því að lesa dálkinn *is_title* úr töflunni *books*. Hugsunin á bakvið forritunina hér var að taka annars vegar nöfn með kommum og hins vegar nöfn án komma, finna mismuninn á þeim og þá var hægt að sjá hversu fjölda komma. Þá er hægt að vita fjölda persóna með því að bæta +1 við fjölda komma. 
**Sem dæmi:** 
Strengurinn Alda, Benni, Elísabet 
Hér eru tvær kommur en nöfnin eru þrjú og þess vegna bætum við +1 við fjölda komma til að vita fjölda persóna.

#### Hversu oft kemur Þengill fyrir í bókunum?
Hér er notað endurtekna CTE (Common Table Expression) með "WITH RECURSIVE" til að skipta streng sem er geymdur í dálkinum *characters* í töflunni *books*. Hún brýtur strenginn upp í einingar aðskildar með kommum og leitar síðan að tilteknu nafni, í þessu tilfelli Þengill. Forritsbúturinn mun síðan skila fjölda raða þar sem nafnið Þengill finnst í dálkinum characters í töflunni books.

**Sem dæmi:** Ef við værum með strenginn Alda, Benni, Elísabet. Þá myndi strengurinn verða að: 
                                Alda, 
                                Benni
                                Elísabet
Forritsbúturinn telur þannig fjölda ákveðins nafns.

#### Hvað eru margir af Paladín ættinni?
Hér telur forritsbúturinn allar raðir í töflunni *family* þar sem *name* dálkurinn inniheldur strenginn "Paladín". Hún skilar heildarfjölda þeirra raða sem innihalda þetta nafn.

#### Hversu algengur er illi arfurinn af þeim sem eru útvalin?
Hér eru allar raðir taldar í töflunni *family* þar sem dálkurinn *chosen_one* hefur gildið "evil". Hún skilar fjölda þeirra raða sem uppfylla þetta skilyrði.


#### Hver er fæðingartíðni kvenna í bókabálkinum?
Eins og við skiljum spurninguna, er verið að spurja um fjölda kvenna sem fæðast á gefnum árum í bókabálkinum.
Forritunin finnur hversu margar konur (gender = 'F') eru fæddar á hverju ári í gagnagrunninum. Hún skilar fjölda fæðinga fyrir hvert ár og birtir það í tímaröð, frá elsta til nýjasta. 

#### Hvað er Ísfólkið margar blaðsíður samanlagt?
Tekur summu allra blaðsíðna (pages) frá töflunni *books*

#### Hvað er meðallengd hvers þáttar af Ískisum?
Þessi fyrirspurn skilar meðallengd(AVG) allra raða í dálkinum *length* úr töflunni *storytel_iskisur* og skilar þá meðallengd hvers þáttar af Ískisum. 

## Til að keyra hina skrána, create_isfolkid.sql 
Það eina sem þarf að skrifa í terminal, eftir að hafa opnað gagnagrunninn, er .schema og þá birtust töflurnar sem unnið var með í liði 2




