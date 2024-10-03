-- Hversu margar aðalpersónur eru í bókabálkinum?
-- 75
WITH RECURSIVE split(characters, str) AS (
    SELECT
        '',
        characters||','
    FROM
        books
    UNION ALL SELECT
        TRIM(substr(str, 0, instr(str, ','))),
        substr(str, instr(str, ',')+1)
    FROM split
    WHERE str != ''
)
SELECT
    COUNT(DISTINCT characters)
FROM split
WHERE characters != '';

-- Hversu margar persónur eru í hverri bók?
/*
Álagafjötrar|2
Nornaveiðar|3
Hyldýpið|1
Vonin|1
Dauðasyndin|2
Illur arfur|3
Draugahöllin|1
Dóttir böðulsins|2
Skuggi fortíðar|2
Vetrarhríð|2
Blóðhefnd|3
Ástarfuni|2
Fótspor Satans|3
Síðasti riddarinn|2
Austanvindar|2
Gálgablómið|3
Garður dauðans|2
Gríman fellur|2
Tennur drekans|1
Hrafnsvængir|3
Um óttubil|3
Jómfrúin og vætturin|3
Vorfórn|4
Í iðrum jarðar|2
Guðsbarn eða galdranorn|3
Álagahúsið|1
Hneykslið|2
Ís og eldur|3
Ástir Lúcífers|3
Ókindin|6
Ferjumaðurinn|2
Hungur|2
Martröð|2
Konan á ströndinni|1
Myrkraverk|1
Galdratungl|4
Vágestur|2
Í skugga stríðsins|2
Raddirnar|2
Fangi tímans|3
Djöflafjallið|1
Úr launsátri|1
Í blíðu og stríðu|1
Skapadægur|1
Böðullinn|3
Svarta vatnið|1
Er einhver þarna úti?|1
*/

SELECT
    is_title,
    LENGTH(characters) - LENGTH(REPLACE(characters, ',', '')) + 1
FROM books;

-- Hversu oft kemur Þengill fyrir í bókunum?
-- 2
WITH RECURSIVE split(characters, str) AS (
    SELECT
        '',
        characters||','
    FROM
        books
    UNION ALL SELECT
        TRIM(substr(str, 0, instr(str, ','))),
        substr(str, instr(str, ',')+1)
    FROM split
    WHERE str != ''
)
SELECT
    COUNT(*)
FROM split
WHERE characters = 'Þengill';


-- Hvað eru margir af Paladín ættinni?
-- Eins og við skiljum spurninguna, er verið að spurja útí fjölskyldunafn og þá í töflunni family (þ.e. ekki characters í books)
-- 9
SELECT COUNT(*) FROM family WHERE name LIKE '%Paladín%';

-- Hversu algengur er illi arfurinn af þeim sem eru útvalin?
-- 18 eru evil af þessum 161 sem eru í töflunni family (19 af þeim eru good). 
SELECT COUNT(*) FROM family WHERE chosen_one='evil';



-- Hver er fæðingartíðni kvenna í bókabálkinum?
-- Eins og við skiljum spurninguna, er verið að spurja um fjölda kvenna sem fæðast á gefnum árum í bókabálkinum.
/*
1556|1
1564|1
1579|1
1583|1
1587|1
1601|2
1602|1
1610|1
1616|1
1627|1
1628|1
1629|1
1634|1
1638|1
1652|1
1655|1
1656|1
1674|1
1677|1
1678|1
1679|1
1694|1
1697|1
1698|1
1699|1
1716|1
1720|1
1750|1
1752|1
1769|1
1775|1
1777|1
1779|1
1788|1
1796|1
1800|2
1820|1
1825|1
1829|1
1830|1
1836|1
1842|1
1848|1
1853|1
1855|1
1872|2
1880|1
1884|1
1894|1
1902|1
1909|1
1910|1
1922|1
1926|1
1929|1
1937|1
1938|1
1942|1
1943|1
1948|1
*/

SELECT birth, COUNT(*) FROM family WHERE gender='F' AND birth IS NOT NULL GROUP BY birth ORDER BY birth ASC;

-- Hvað er Ísfólkið margar blaðsíður samanlagt?
-- 8023

SELECT SUM(pages) FROM books;

--Hvað er meðallengd hvers þáttar af Ískisum?
--116.40206185567
SELECT AVG(length) FROM storytel_iskisur;