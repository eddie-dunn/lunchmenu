#!/usr/bin/env python
# pylint: disable=missing-docstring
# pylint: disable=invalid-name
from collections import defaultdict
import datetime

import requests
from bs4 import BeautifulSoup

DAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
        'sunday')

NAME = 'Edison'


def get_menu_html():
    result = requests.get('http://restaurangedison.se/lunch')
    if result.status_code != 200:
        raise Exception(result.status_code)
    return result.content


def get_menu(contents):
    soup = BeautifulSoup(contents, 'lxml')
    menu = defaultdict(dict)
    for day in DAYS[:-2]:
        meals = {}
        info = soup.body.find('div', attrs={'id': day})
        table = info.find('table')
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            meal = ': '.join([col.text for col in cols[:-1]])
            meal = f'{cols[0].text}: {cols[1].text}'
            meal_type = cols[0].text
            meal = cols[1].text
            meals[meal_type] = meal

        menu[day] = meals
    return menu


def get_menu_of_the_day(today=None):
    today = today or datetime.datetime.today().weekday()
    try:
        contents = get_menu_html()
    except Exception as e:  # pylint: disable=broad-except
        return {'error': str(e)}

    menu = get_menu(contents)
    return menu[DAYS[today]]


def _title():
    today = datetime.datetime.today().weekday()
    week = datetime.datetime.now().isocalendar()[1]
    dag = ('måndag', 'tisdag', 'onsdag', 'torsdag', 'fredag')
    title = f'Edison, v{week}, {dag[today]}'
    return title + '\n' + '=' * len(title)


def main():
    todays_menu = get_menu_of_the_day()
    print(_title())
    for key, val in todays_menu.items():
        print(f'{key}: {val}')


def api_menu():
    menu = get_menu_of_the_day()
    if 'error' in menu:
        return {
            'restaurant': 'Edison', 'courses': [], 'error': menu['error']
        }

    courses = [
        {'name': name, 'description': descr}
        for name, descr in menu.items()
    ]

    return {
        'restaurant': 'Edison',
        'courses': courses,
    }


if __name__ == '__main__':
    # main()
    import json
    print(json.dumps(api_menu()))
