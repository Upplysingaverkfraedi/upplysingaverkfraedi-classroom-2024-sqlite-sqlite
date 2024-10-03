import re
import sqlite3
import requests

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        sanitized_filename = re.sub(r'[\/:*?"<>|&=]', '_', url.split('/')[-1])
        with open(f"debug_{sanitized_filename}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)  # Save HTML content for inspection
        return html_content
    else:
        print(f"Ekki tókst að sækja gögn af {url}")
        return None

def parse_links(html, base_url):
    links = re.findall(r'href="(urslit/\?race=\d+&cat=[^"]+)"', html)
    full_links = [base_url + link for link in links]
    return full_links

def parse_results(html):
    table_match = re.search(r'<table.*?>.*?</table>', html, re.DOTALL)
    
    if table_match:
        table_html = table_match.group(0)
        rows = re.findall(r'<tr.*?>(.*?)</tr>', table_html, re.DOTALL)

        data = []
        for row in rows:
            columns = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)
            if columns:
                column_data = [re.sub(r'<.*?>', '', col).strip() for col in columns]
                data.append(column_data)
        
        return data
    else:
        print("Engin tafla fannst í úrslitunum.")
    return []

def parse_participant_count(html, race_category):
    # Sérstök meðhöndlun fyrir 'overall'
    if race_category == 'overall':
        match = re.search(r'(\d+) participants', html)
        if match:
            print(f"Heildarfjöldi keppenda fundinn: {match.group(1)}")
            return int(match.group(1))
    
    # Leitar að línunni með "Started / Finished" og tekur fjöldann sem hóf hlaupið
    match = re.search(r'Started / Finished</small>\s*<h4>(\d+)\s*/\s*\d+</h4>', html)
    
    if match:
        print(f"Found 'Started / Finished': {match.group(1)} keppendur byrjuðu hlaupið")
        return int(match.group(1))  # Skilar fjölda keppenda sem hófu hlaupið
    else:
        # Bæta við sérstakri meðhöndlun fyrir "150" fjöldann
        match_overall = re.search(r'<h4>(150)</h4>', html)
        if match_overall:
            print(f"Found 'Overall Participants' set to 150: {match_overall.group(1)} keppendur")
            return int(match_overall.group(1))

        print("Ekki tókst að finna fjölda keppenda. Nota 0 sem sjálfgefið gildi.")
    return 0  # Ef engin tala finnst, skilar 0

def skrifa_nidurstodur(data, db_file, race_name, race_start, race_end, participant_count):
    if not data:
        print(f"Engar niðurstöður til að skrifa fyrir {race_name}.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

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

    cursor.execute('''
    SELECT id FROM hlaup WHERE nafn = ? AND upphaf = ?
    ''', (race_name, race_start))

    hlaup_id = cursor.fetchone()
    if hlaup_id:
        hlaup_id = hlaup_id[0]
    else:
        cursor.execute('''
        INSERT INTO hlaup (upphaf, endir, nafn, fjoldi)
        VALUES (?, ?, ?, ?)
        ''', (race_start, race_end, race_name, participant_count))
        hlaup_id = cursor.lastrowid

    for row in data:
        if len(row) >= 3:
            name = row[0]
            time = row[1]
            gender = row[2] if len(row) > 2 else None
            age = int(row[3]) if len(row) > 3 and row[3].isdigit() else None

            cursor.execute('''
            SELECT id FROM timataka WHERE hlaup_id = ? AND nafn = ? AND timi = ?
            ''', (hlaup_id, name, time))

            if not cursor.fetchone():
                cursor.execute('''
                INSERT INTO timataka (hlaup_id, nafn, timi, kyn, aldur)
                VALUES (?, ?, ?, ?, ?)
                ''', (hlaup_id, name, time, gender, age))

    conn.commit()
    conn.close()
    print(f"Niðurstöður fyrir {race_name} vistaðar í {db_file}.")

def main():
    db_file = "results.db"

    base_url = "https://timataka.net/criterium2022_islandsmot/"
    start_page = base_url

    html = fetch_html(start_page)
    if not html:
        print("Ekki tókst að sækja upphafssíðuna.")
        return

    result_links = parse_links(html, base_url)

    for link in result_links:
        print(f"Sæki gögn af {link}")
        result_html = fetch_html(link)
        if not result_html:
            print(f"Ekki tókst að sækja gögn af {link}")
            continue

        data = parse_results(result_html)

        race_name = link.split('cat=')[-1]
        race_start = '2022-08-28 10:00:00'
        race_end = '2022-08-28 12:00:00'

        participant_count = parse_participant_count(result_html, race_name)
        print(f"Fjöldi keppenda fyrir {race_name}: {participant_count}")

        skrifa_nidurstodur(data, db_file, race_name, race_start, race_end, participant_count)

if __name__ == "__main__":
    main()
