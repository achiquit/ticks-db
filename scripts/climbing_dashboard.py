import sqlite3
from sqlite3 import Cursor
from jinja2 import Environment, FileSystemLoader
import os

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

def height_goodies(feet: int, transforms: list) -> dict:
    returns = {}

    for item in transforms:
        ans = feet / item[1]
        returns[item[0]] = "{:,.0f}".format(ans)
    
    return returns

def pitches_func(cur: Cursor) -> int:
    res = cur.execute("""
        SELECT
            SUM(pitches)
        FROM
            ticks;
    """)

    res = res.fetchall()

    to_add = "{:,.0f}".format(res[0][0])

    return to_add

def climbs_func(cur: Cursor) -> int:
    res = cur.execute("""
        SELECT
            COUNT(DISTINCT climb)
        FROM
            ticks;
    """)

    res = res.fetchall()

    to_add = "{:,.0f}".format(res[0][0])

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

def areas_func(cur: Cursor) -> int:
    res = cur.execute("""
        SELECT
            COUNT(DISTINCT area)
        FROM
            ticks
            INNER JOIN climbs ON ticks.climb = climbs.id;
    """)

    res = res.fetchall()

    to_add = "{:,.0f}".format(res[0][0])

    return to_add

def partners_func(cur: Cursor) -> int:
    res = cur.execute("""
        SELECT
            COUNT(DISTINCT id)
        FROM
            partners
    """)

    res = res.fetchall()

    to_add = "{:,.0f}".format((res[0][0] - 5))

    return to_add

def main():

    con = sqlite3.connect("ticks")
    cur = con.cursor()

    env = Environment(loader = FileSystemLoader('../websitejazzhands/templates'))
    template = env.get_template('climbing_dashboard.html')

    items = []

    transforms = [
        ["feet", 1], 
        ["meters", 3.2808], 
        ["Eiffel Towers", 1083], 
        ["bananas", 0.5833],
        # To finish adding below here
        ["fathoms", 6],
        ["cubits", 1.5],
        ["Andres", 5.92],
        ["El Capitans", 3000],
        ["miles", 5280]
    ]
    vals = []

    items.append(height_func(cur))
    items.append(pitches_func(cur))
    items.append(climbs_func(cur))
    items.append(days_func(cur))
    items.append(areas_func(cur))

    height = items[0][1]

    transforms = height_goodies(height, transforms)

    with open(f'../websitejazzhands/climbing/index.html', 'w+') as f:
        print(template.render(
            feet_unit = "feet",
            feet_num = transforms["feet"],
            meter_unit = "meters",
            meter_num = transforms["meters"],
            eiffel_unit = "Eiffel Towers",
            eiffel_num = transforms["Eiffel Towers"],
            banana_unit = "bananas",
            banana_num = transforms["bananas"],
            fathoms_unit = "fathoms",
            fathoms_num = transforms["fathoms"],
            cubits_unit = "cubits",
            cubits_num = transforms["cubits"],
            andres_unit = "Andres",
            andres_num = transforms["Andres"],
            el_cap_unit = "El Capitans",
            el_cap_num = transforms["El Capitans"],
            miles_unit = "miles",
            miles_num = transforms["miles"],
            pitches = pitches_func(cur),
            climbs = climbs_func(cur),
            areas = areas_func(cur),
            partners = partners_func(cur)
        ), file = f)

if __name__ == '__main__':
    main()