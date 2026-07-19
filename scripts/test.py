import sqlite3
from sqlite3 import Cursor
from jinja2 import Environment, FileSystemLoader
import os

con = sqlite3.connect("ticks")
cur = con.cursor()

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('climbing_dashboard.html')

if not os.path.exists(f"../websitejazzhands/climbing/test"):
    os.makedirs(f"../websitejazzhands/climbing/test")

items = []

transforms = [
    ["Feet", 1], 
    ["Meters", 3.2808], 
    ["Eiffel Towers", 1083], 
    ["Bananas", 0.5833]
]
keys = []
values = []

def height_func(cur: Cursor) -> list:
    res = cur.execute("""
        SELECT
            SUM(height)
        FROM
            ticks;
    """)

    res = res.fetchall()

    height = ["height"]

    height += list(res[0])

    return height

def height_goodies(feet: int, transforms: list) -> list:
    returns = []

    for item in transforms:
        ans = feet / item[1]
        keys.append(item[0])
        values.append(ans)
    
    return returns

def pitches_func(cur: Cursor) -> list:
    res = cur.execute("""
        SELECT
            SUM(pitches)
        FROM
            ticks;
    """)

    res = res.fetchall()

    to_add = ["pitches"]

    to_add += list(res[0])

    return to_add

def climbs_func(cur: Cursor) -> list:
    res = cur.execute("""
        SELECT
            COUNT(DISTINCT climb)
        FROM
            ticks;
    """)

    res = res.fetchall()

    to_add = ["climbs"]

    to_add += list(res[0])

    return to_add

def days_func(cur: Cursor) -> list:
    res = cur.execute("""
        SELECT
            COUNT(DISTINCT date)
        FROM
            ticks;
    """)

    res = res.fetchall()

    to_add = ["days"]

    to_add += list(res[0])

    return to_add

def areas_func(cur: Cursor) -> list:
    res = cur.execute("""
        SELECT
            COUNT(DISTINCT area)
        FROM
            ticks
            INNER JOIN climbs ON ticks.climb = climbs.id;
    """)

    res = res.fetchall()

    to_add = ["areas"]

    to_add += list(res[0])

    return to_add

items.append(height_func(cur))
items.append(pitches_func(cur))
items.append(climbs_func(cur))
items.append(days_func(cur))
items.append(areas_func(cur))

height = items[0][1]

fun = height_goodies(height, transforms)

with open(f'../websitejazzhands/climbing/test/index.html', 'w+') as f:
    print(template.render(), file = f)