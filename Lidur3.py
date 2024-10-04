import requests
import re
import pandas as pd
from datetime import datetime

# Constants
TIMATAKA_URL = 'https://timataka.net/'
RACE_DATES = "Aug 2022"

# Regex
GROUP_RACES_BY_DATE = r'<h3>(.*?)<\/h3>((?:\s*<li>(?:.|\n)*?<\/li>\s*)*)'
GET_RACE_LINK_AND_NAME = r'<li><a href="(.*?)">([\s\S]*?)<\/a>\s*\((.*?)\)<\/li>'
GET_RACE_NUMBERS = r'<a href="urslit\/\?race=([0-9]*)&.*">.*<\/a><br\/>'
GET_RACE_NAME = r'<h2>\s*([\s\S]*?)<\/h2>'
GET_RACE_START_TIME = r'<small class="stats-label">Start time<\/small>\s*<h4>(.*?)<\/h4>'
GET_RACE_END_TIME = r'<small class="stats-label">Est\. finish time<\/small>\s*<h4>(.*?)<\/h4>'
GET_RACE_NUMBER_OF_COMPETITORS = r'<small class="stats-label">Started \/ Finished<\/small>\s*<h4>(.*?) \/ .*<\/h4>'
GET_YEAR_FROM_MONTH_YEAR = r'((?:.*){3}) ([0-9]{4})'
GET_DAY_FROM_DATE = r'([0-9]*).*'

def get_dates_races():
    '''This is a function that gets all of the dates on the website'''

    response = requests.get(TIMATAKA_URL)
    text = response.text

    race_groups = re.findall(GROUP_RACES_BY_DATE, text)

    races = []
    for month_year, group_html in race_groups:
        race_link_name = re.findall(GET_RACE_LINK_AND_NAME, group_html)

        for link, name, date in race_link_name:
            month, year = re.findall(GET_YEAR_FROM_MONTH_YEAR, month_year)[0]
            day = re.findall(GET_DAY_FROM_DATE, date)[0]
            date_str = f"{day} {month} {year}"
            date_object = datetime.strptime(date_str, "%d %b %Y")

            races.append((date_object, name, link))

    df = pd.DataFrame(races, columns=['Date', 'Name', 'Link'])
    return df

def filter_races(df):
    '''Filter out all the races that are not neccessary'''

    df = df[df['Date'] == RACE_DATES]
    return df

def get_race_numbers(url):
    '''Gets unique race numbers given a url'''
    
    response = requests.get(url)
    text = response.text

    race_numbers = re.findall(GET_RACE_NUMBERS, text)
    unique_race_numbers_set = set(race_numbers)
    unique_race_numbers = list(unique_race_numbers_set)

    return unique_race_numbers

def get_sub_race_link(url, race_number):
    return url + "/urslit?race=" + race_number

def get_race_info(url):
    '''This gets the basic race info given a url'''

    response = requests.get(url)
    text = response.text

    race_name = re.findall(GET_RACE_NAME, text)[0]
    start_time = re.findall(GET_RACE_START_TIME, text)[0]
    end_time = re.findall(GET_RACE_END_TIME, text)[0]
    number_of_competitors = re.findall(GET_RACE_NUMBER_OF_COMPETITORS, text)[0]

    return race_name, start_time, end_time, number_of_competitors

def get_races_from_events(df):
    all_races = []
    for _, row in df.iterrows():
        link = row['Link']
        race_numbers = get_race_numbers(link)
        
        for race_number in race_numbers:
            sub_race_link = get_sub_race_link(link, race_number)
            sub_race_info = get_race_info(sub_race_link)
            
            all_races.append((row['Name'], row['Date']) + sub_race_info)

    df_all_races = pd.DataFrame(all_races, columns=['vidburdur', 'nafn', 'upphaf', 'endir', 'fjoldi'])
    return df_all_races

def main():
    '''This is the main function'''
    
    df = get_dates_races()
    df = filter_races(df)
    df = get_races_from_events(df)

    print(df)

    df.to_csv('hlaup.csv', index=None)

if __name__ == '__main__':
    main()