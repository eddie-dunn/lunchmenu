"""Restaurant Menus webapp.

Done:
    * Simple plugin system
    * Fetch from sample restaurant (Edison)
    * Use cache

TODOs:

    * Docker image
    * even with cache, restaurants that may have only temporary errors should
      be refetched
    * Set cache timeout in seconds since last fetch, rather than for new days
    * Async fetch of restaurant data

"""
# pylint: disable=missing-docstring
import datetime
import json
import os
import subprocess

from flask import Flask
from flask import jsonify


app = Flask(__name__)  # pylint: disable=invalid-name

LAST_FETCHED = (1900, 1, 1)
PLUGIN_PATH = './plugs'
CACHE_ENABLED = True

CACHE = {'last_fetched': (1900, 1, 1), 'saved_menus': None}
CACHE_TIMEOUT = 60*60*3  # two hour timeout
SAVED_MENUS = None


def find_execs(path: str) -> list:
    """Return a list of executables found in `path`"""
    execs = []
    for filename in os.listdir(path):
        filepath = os.path.abspath(os.path.join(path, filename))
        if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
            execs.append(filepath)
    return execs


def run(filename: str) -> dict:
    """Run `filename`, return stdout"""
    try:
        app.logger.debug(f"running {filename}")
        result = subprocess.check_output(filename).decode()
        return json.loads(result)
    except json.JSONDecodeError:
        app.logger.exception(f'COULD NOT DECODE: {result}')
        error_menu = {
            'restaurant': 'Error Test Restaurant',
            'courses': [],
            'error': 'Couldn\'t fetch',
        }
        return error_menu
    return result


def plugged_menus(path: str = PLUGIN_PATH) -> list:
    plugins = find_execs(path)
    menus = [run(plugin) for plugin in plugins]
    app.logger.info("Got the following menus: %r", menus)
    return menus


def should_update_cache(date: datetime.datetime) -> bool:
    """Return True if cache should be updated"""
    return bool(
        (date.year, date.month, date.day) > CACHE['last_fetched']
        or not CACHE['saved_menus']
        or not CACHE_ENABLED
    )

def fetch_menus():
    date = datetime.datetime.now()
    if not should_update_cache(date):
        app.logger.info("Using cached result")
        return CACHE['saved_menus']

    # reset date to today, in order to cache the results of the day
    CACHE['last_fetched'] = (date.year, date.month, date.day)

    # get menus of the day
    menus = plugged_menus()
    # save menus to cache
    CACHE['saved_menus'] = menus
    return menus


# Functions to render html; should be replaced later
def course_render(courses: dict) -> str:
    courses_html = [
        f"<strong>{course['name']}</strong> {course['descr']}<br>"
        for course in courses
    ]
    return ''.join(courses_html)


def render_menus(menus_list: list) -> dict:
    menus = []
    for elem in menus_list:
        menus.append((
            f"<h3>{elem['restaurant']}</h3>"
            f"{course_render(elem['courses'])}"
        ))
    return ''.join(menus)


# Routes
@app.route('/')
def root():
    return render_menus(fetch_menus())


@app.route('/api/v1/menus')
def api_menus():
    return jsonify(fetch_menus())
