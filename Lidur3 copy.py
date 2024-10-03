import requests
import pandas as pd
import argparse
import re

def parse_html(html):
    # Regluleg segð til að finna allar <tr> töflur
    row_pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
    # Regluleg segð til að finna <td> innan hverrar <tr> töflu
    column_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)

    rows = row_pattern.findall(html)
   
    # Sækir gögn frá öllum línum 
    data = []
    for row in rows:
        columns = column_pattern.findall(row)
        columns = [re.sub(r'<[^>]+>', '', column).strip() for column in columns]
        if columns:  
            data.append(columns)
    
    return data

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_runs_by_date():
    '''Get all of the runs by date'''

    response = requests.get("https://timataka.net")
    soup = BeautifulSoup(response.text, features="html.parser")
    headings = soup.find_all('h3')
    
    run_url = []
    for heading in headings:
        date_str = heading.text
        date_obj = datetime.strptime(date_str, "%b %Y")

        if date_obj.year == 2022 and date_obj.month == 8:
            sibling = heading.find_next_sibling()
            
            while sibling.name == 'li':
                url = sibling.find('a')
                run_url.append(url['href'])
                sibling = sibling.find_next_sibling()

    return run_url

from urllib.parse import urljoin
def get_all_race_types(url):
    '''This gets all of the different race types'''

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    title = soup.find('h2')
    container = soup.find('div', {'class': 'container'})


    links = [urljoin(url + "/", a['href']) for a in container.find_all('a')]

    return title.text, links

def get_race(url):
    response = requests.get(url)
    html_text = response.text

    parsed_html = parse_html(html_text)
    return parsed_html

def get_dataframe_all_races():
    all_results = []

    all_races = get_runs_by_date()
    for race in all_races:
        title, race_types = get_all_race_types(race)
        for race_type in race_types:
            race_result = get_race(race_type)

            for r in race_result:
                all_results.append(r + [title])

    df = pd.DataFrame(all_results)
    return df

def main():
    df = get_dataframe_all_races()
    df.to_csv('races.csv')

if __name__ == "__main__":
    main()