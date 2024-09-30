import requests
import pandas as pd
import argparse
import re
import sqlite3
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
    row_pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
    column_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)

    rows = row_pattern.findall(html)
    data = []
    for row in rows:
        columns = column_pattern.findall(row)
        columns = [re.sub(r'<[^>]+>', '', column).strip() for column in columns]
        if columns:
            data.append(columns)
    
    return data

def skrifa_nidurstodur(data, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Býr til hlaup og timataka töflur ef þær eru ekki til
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
        FOREIGN KEY (hlaup_id) REFERENCES hlaup(id)
    )
    ''')

    # Fylki af keppendum
    if not data:
        print("Engar niðurstöður til að skrifa.")
        return
    
    # Hér þarftu að fylla inn gögn fyrir hlaup, þ.e. upphaf, endir, nafn, fjöldi
    # Setjum inn sýnidæmi fyrir hlaup
    hlaup_nafn = "Flensborgarhlaupið 2022"
    upphaf = datetime(2022, 8, 5, 10, 0)  # Dæmi
    endir = datetime(2022, 8, 5, 12, 0)   # Dæmi
    fjoldi = len(data)

    cursor.execute('''
    INSERT INTO hlaup (upphaf, endir, nafn, fjoldi)
    VALUES (?, ?, ?, ?)
    ''', (upphaf, endir, hlaup_nafn, fjoldi))

    hlaup_id = cursor.lastrowid

    # Bætum við keppendum
    for keppandi in data:
        nafn = keppandi[0]
        timi = keppandi[1]
        kyn = keppandi[2] if len(keppandi) > 2 else None
        aldur = keppandi[3] if len(keppandi) > 3 else None

        cursor.execute('''
        INSERT INTO timataka (hlaup_id, nafn, timi, kyn, aldur)
        VALUES (?, ?, ?, ?, ?)
        ''', (hlaup_id, nafn, timi, kyn, aldur))

    conn.commit()
    conn.close()
    print(f"Niðurstöður vistaðar í '{db_file}'.")

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
        with open(html_file, 'w') as file:
            file.write(html)
        print(f"HTML fyrir {args.url} vistað í {html_file}")

    results = parse_html(html)
    skrifa_nidurstodur(results, args.output)

if __name__ == "__main__":
    main()
