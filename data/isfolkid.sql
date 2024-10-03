

-- Hversu margar aðalpersónur eru í bókabálkinum?
SELECT 'Aðalpersónur: ' || COUNT(*) FROM books WHERE characters <> '';

----- Segjum að það sé ein aðalpersóna í hverri bók því ég veit ekki hvar maður sér aðalpersónur
----- og þetta skilar hversu margar línur eru þar sem characters er ekki tómur og 
----- þ.a.l. hversu margar aðalpersónur eru


-- Hversu margar persónur eru í hverri bók?
SELECT 'Persónur í hverri bók: ' || 
  id, 
  is_title, 
  LENGTH(characters) - LENGTH(REPLACE(characters, ',', '')) + 1
FROM books;

-----þetta telur hversu margir characters eða persónur eru í hverri bók og 
-----skilar númerinu á bókinni svo nafninu á bókinni og svo fjölda persóna


-- Hversu oft kemur Þengill fyrir í bókunum?
SELECT 'Þengill: ' || COUNT(*) FROM books WHERE characters LIKE '%Þengill%';

-- Hvað eru margir af Paladín ættinni?
SELECT 'Paladín: ' || COUNT(*) FROM family WHERE name LIKE '%Paladín%';

-- Hversu algengur er illi arfurinn af þeim sem eru útvalin? 
SELECT 'Illi arfurinn: ' || COUNT(*) FROM family WHERE chosen_one LIKE 'evil';

-- skilar hversu oft evil kemur fyrir í chosen_one

-- Hver er fæðingartíðni kvenna í bókabálkinum? 
SELECT 'Fæðingartíðni: ' || AVG(birth) FROM family WHERE gender LIKE 'F';

-----Meðaltal á birth hjá konum (F)

-- Hvað er Ísfólkið margar blaðsíður samanlagt?
 SELECT 'Blaðsíður: ' || SUM(pages) FROM books;

-- Hvað er meðallengd hvers þáttar af Ískisum?
SELECT 'Meðallengd: ' || AVG(length) FROM storytel_iskisur;

