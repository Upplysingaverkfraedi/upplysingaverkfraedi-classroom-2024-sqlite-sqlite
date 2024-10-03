from bs4 import BeautifulSoup
import requests
import sqlite3
import argparse
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description='Vinna með úrslit af tímataka.net.')
    parser.add_argument('--url', help='Slóð að vefsíðu með úrslitum.')
    parser.add_argument('--output', required=True, help='Slóð að SQLite gagnagrunni.')
    parser.add_argument('--debug', action='store_true', help='Vistar html í skrá til að skoða.')
    return parser.parse_args()

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Tókst ekki að sækja gögn af {url}")
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')  # Finna fyrstu töflu á síðunni

    data = []
    if table:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            column_data = [col.get_text(strip=True) for col in columns]
            if column_data:
                data.append(column_data)

    return data

def skrifa_nidurstodur(data, db_file, race_name, race_start, race_end, participant_count):
    if not data:
        print("Engar niðurstöður til að skrifa.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Búa til töflur ef þær eru ekki til
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hlaup (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        upphaf DATETIME NOT NULL,
        endir DATETIME,
        nafn TEXT NOT NULL,
        fjoldi INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS timataka (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hlaup_id INTEGER,
        nafn TEXT NOT NULL,
        timi TEXT NOT NULL,
        kyn TEXT,
        aldur INTEGER,
        UNIQUE(hlaup_id, nafn, timi),
        FOREIGN KEY (hlaup_id) REFERENCES hlaup(id)
    )
    ''')

    # Setja inn hlaupið (upplýsingar dregnar úr HTML gögnum)
    cursor.execute('''
    INSERT INTO hlaup (upphaf, endir, nafn, fjoldi)
    VALUES (?, ?, ?, ?)
    ''', (race_start, race_end, race_name, participant_count))

    # Nýlega sett hlaup_id fyrir hlaupið
    hlaup_id = cursor.lastrowid

    # Setja inn niðurstöður þátttakenda í hlaupið
    for row in data:
        if len(row) >= 3:
            name = row[0]
            time = row[1]
            gender = row[2] if len(row) > 2 else None
            age = int(row[3]) if len(row) > 3 and row[3].isdigit() else None

            cursor.execute('''
            INSERT INTO timataka (hlaup_id, nafn, timi, kyn, aldur)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(hlaup_id, nafn, timi) DO NOTHING
            ''', (hlaup_id, name, time, gender, age))

    conn.commit()
    conn.close()
    print(f"Niðurstöður fyrir {race_name} hafa verið vistaðar í {db_file}.")

def verify_participant_counts(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT h.nafn, h.fjoldi AS skradir_keppendur, COUNT(t.id) AS raunverulegir_keppendur
    FROM hlaup h
    LEFT JOIN timataka t ON h.id = t.hlaup_id
    GROUP BY h.id;
    ''')

    results = cursor.fetchall()
    for result in results:
        print(f"{result[0]}: Skráðir keppendur: {result[1]}, Raunverulegir keppendur: {result[2]}")

    conn.close()

def main():
    args = parse_arguments()

    if not ('timataka.net' in args.url and 'urslit' in args.url):
        print("Slóðin er ekki frá timataka.net eða ekki með úrslitum.")
        return

    html = fetch_html(args.url)
    if not html:
        raise Exception("Ekki tókst að sækja HTML gögn, athugið URL.")

    if args.debug:
        html_file = args.output.replace('.sqlite', '.html')
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(html)
        print(f"HTML fyrir {args.url} vistað í {html_file}")

    # Dæmi um að ná í mörg hlaup frá ágúst 2022 (þar sem upplýsingarnar eru fengnar af síðunni)
    # Upplýsingarnar eins og nafn hlaupsins, upphafs- og loktími og fjöldi þátttakenda ættu að vera dregnar
    # af tímataka.net síðunni, t.d. með aðra töflu eða div.
    race_name = "Ljósanæturhlaup Lífsstíls"
    race_start = '2022-08-31 18:00:00'
    race_end = '2022-08-31 20:00:00'
    participant_count = 200  # Þessi tala verður að koma úr raunverulegum gögnum

    results = parse_html(html)
    skrifa_nidurstodur(results, args.output, race_name, race_start, race_end, participant_count)
    verify_participant_counts(args.output)

if __name__ == "__main__":
    main()
