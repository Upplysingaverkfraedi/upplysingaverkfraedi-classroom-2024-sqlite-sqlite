from bs4 import BeautifulSoup
import requests
import pandas as pd
import argparse
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

def skrifa_nidurstodur(data, db_file):
    if not data:
        print("Engar niðurstöður til að skrifa.")
        return

    # Hérna kemur restin af SQLite kóðanum til að vista gögnin í gagnagrunninn
    # Síðan er unnið með 'data' eins og áður var útskýrt
    # ...

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

    results = parse_html(html)
    skrifa_nidurstodur(results, args.output)

if __name__ == "__main__":
    main()
