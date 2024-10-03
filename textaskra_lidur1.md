# Nánari útskýringar á lið 1 

## Taflan `names.sql`: 

Taflan `names.sql` geymir upplýsingar um bæði eiginnöfn og millinöfn ásamt tíðni þeirra. Dálkarnir í töflunni eru skilgreindir á eftirfarandi hátt:
* `name`: Þetta er nafn einstaklingsins, tekið er tillit til bæði eiginnafns og millinafns. Gagnategundin er text vegna þess að nafn er alltaf strengur.
* `year`: Ár sem nafnið kemur fyrir, skilgreint sem int.
* `frequency`: Tíðni nafnsins það árið, sem er einnig int.
* `type`: Tegund nafns, þar sem gildin eru annaðhvort “eiginnafn” eða “millinafn”.

## Greining á gögnum: 

### Hvaða hópmeðlimur á algengasta eiginnafnið?
Hér er leitað að nafni með hæsta gildi í dálkinum frequency þar  nafnið hefur tegundina (type) „eiginnafn“ vegna þess að við viljum bara fá eiginnafn ekki millinafn.
### Hvenær voru öll nöfnin vinsælust?
Hér er leitað eftir árinu þar sem samanlagður fjöldi allra nafna var hæstur. Þetta er gert með því að summu upp frequency fyrir hvert einasta ár.
### Hvenær komu þau fyrst fram?
Til að finna hvenær nöfnin komu fyrst fram, leitum við að lægsta gildi í year dálknum fyrir hvert nafn.
