import re
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        with open(f"debug_{url.split('/')[-1]}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)  # Save the HTML content for inspection
        return html_content
    else:
        print(f"Ekki tókst að sækja gögn af {url}")
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Adjust based on actual HTML structure
    table = soup.find('table')  # Find the first table on the page

    if not table:
        print("Engin tafla fannst.")
        return []

    data = []
    
    # Extract the rows
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        if columns:
            column_data = [col.get_text(strip=True) for col in columns]
            if column_data:
                data.append(column_data)

    return data

def skrifa_nidurstodur(data, db_file, race_name, race_start, race_end, participant_count):
    if not data:
        print(f"Engar niðurstöður til að skrifa fyrir {race_name}.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the 'hlaup' table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hlaup (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        upphaf DATETIME NOT NULL,
        endir DATETIME,
        nafn TEXT NOT NULL,
        fjoldi INTEGER,
        UNIQUE(nafn, upphaf)
    )
    ''')

    # Create the 'timataka' table if it doesn't exist
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

    # Insert race details
    cursor.execute('''
    INSERT OR IGNORE INTO hlaup (upphaf, endir, nafn, fjoldi)
    VALUES (?, ?, ?, ?)
    ''', (race_start, race_end, race_name, participant_count))

    hlaup_id = cursor.lastrowid

    # Insert participants
    for row in data:
        if len(row) >= 3:
            name = row[0]
            time = row[1]
            gender = row[2] if len(row) > 2 else None
            age = int(row[3]) if len(row) > 3 and row[3].isdigit() else None

            cursor.execute('''
            INSERT OR IGNORE INTO timataka (hlaup_id, nafn, timi, kyn, aldur)
            VALUES (?, ?, ?, ?, ?)
            ''', (hlaup_id, name, time, gender, age))

    conn.commit()
    conn.close()
    print(f"Niðurstöður fyrir {race_name} vistaðar í {db_file}.")

def main():
    db_file = "results.db"  # SQLite database file

    # List of URLs for all August 2022 races
    urls = [
        "https://timataka.net/ljosanaeturhlaup2022",
        "https://timataka.net/criterium2022_islandsmot",
        "https://timataka.net/tindahlaup2022/",
        "https://timataka.net/sprettthraut2022",
        "https://timataka.net/landsnet2022/",
        "https://timataka.net/fossvogshlaupid2022/",
        "https://timataka.net/fellahringurinn2022/",
        "https://timataka.net/hundahlaupid2022/",
        "https://timataka.net/skalafell2022",
        "https://timataka.net/reykjavikurmarathon2022",
        "https://timataka.net/grefillinn2022",
        "https://timataka.net/criterium2022_2",
        "https://timataka.net/ormurinn2022/",
        "https://timataka.net/trekyllisheidin2022/",
        "https://timataka.net/5vh-hlaup-2022",
        "https://timataka.net/enduroiso2022",
        "https://timataka.net/stelpuhringur2022/",
        "https://timataka.net/criterium2022_1",
        "https://timataka.net/morgunbladshringurinn2022",
        "https://timataka.net/austurultra2022",
        "https://timataka.net/bruarhlaupid2022/",
        "https://timataka.net/jokulsarhlaup2022/",
        "https://timataka.net/posthlaupid2022",
        "https://timataka.net/castelli-classic-rr-2022",
        "https://timataka.net/vatnsmyrarhlaupid2022",
        "https://timataka.net/tt2022_4"
    ]

    for url in urls:
        html = fetch_html(url)
        if not html:
            print(f"Ekki tókst að sækja gögn af {url}")
            continue

        # Example: Replace with dynamic fetching if needed
        race_name = url.split('/')[-1]  # Use URL fragment as the race name for now
        race_start = '2022-08-01 10:00:00'  # Replace with actual start time
        race_end = '2022-08-01 12:00:00'  # Replace with actual end time
        participant_count = 150  # Replace with actual participant count

        data = parse_html(html)
        skrifa_nidurstodur(data, db_file, race_name, race_start, race_end, participant_count)

if __name__ == "__main__":
    main()
