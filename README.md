Fyrir dæmi 1 þarf að huga að eftirfarandi atriðum til að fá kóðann til að virka.

1. Fá SQLite inn í kerfið (ef það er nú þegar ekki til staðar).

Fyrir macOS/linux:

brew install sqlite

Fyrir window notanda:

Þá er hlaðið inn SQLite frá síðunni:
https://www.sqlite.org/download.html

2. Búa til eða nota SQLite gagngagrunn skrá

Notandinn þarf SQLite gagngagrunn skrá til að keyra fyrirspurnina. Hér heitir gagnaskráin
names_freq.db og taflan names er búin til innan hennar.

3. Verður að hafa tvær skrár sem innihalda nöfnin sem gögnin eru sótt í. Önnur heitir
first_names_freq.csv hin heitir middle_names_freq.csv.

4. Með kóðanum úr dæmi eitt er farið inn í terminalið og keyrt skipunana
 ```sqlite3 data/names_freq.db < names.sql ```


