import sqlite3
from sqlite3 import Cursor
from jinja2 import Environment, FileSystemLoader
import os

def partner_list() -> list:
    ### Make sure to remove the counter from the for loop to get all partners ###

    partners = []

    res = cur.execute(f"""
        SELECT
            id,
            fname,
            lname
        FROM
            partners
    """)

    counter = 0
    for item in res:
        partners += [list(item)]
        counter += 1
        if counter > 5:
            break
    
    return partners

def area_func(cur: Cursor, partner: int) -> int:
    res = cur.execute(f"""
        SELECT
            COUNT(DISTINCT climbs.area)
        FROM ticks
        INNER JOIN climbs ON ticks.climb = climbs.id
        INNER JOIN climbed_partners ON ticks.climbed_id = climbed_with.climbing_id
        JOIN climbed_with ON climbed_partners.id = climbed_with.climbing_id
        JOIN partners ON climbed_with.partner_id = partners.id
        WHERE partners.id = {partner}
    """)

    for item in res:
        return item[0]

def days_func(cur: Cursor, partner: int) -> int:
    res = cur.execute(f"""
        SELECT
            COUNT(DISTINCT ticks.date)
        FROM ticks
        INNER JOIN climbs ON ticks.climb = climbs.id
        INNER JOIN climbed_partners ON ticks.climbed_id = climbed_with.climbing_id
        JOIN climbed_with ON climbed_partners.id = climbed_with.climbing_id
        JOIN partners ON climbed_with.partner_id = partners.id
        WHERE partners.id = {partner}
    """)

    for item in res:
        return item[0] 

def pitches_func(cur: Cursor, partner: int) -> int:
    res = cur.execute(f"""
        SELECT
            SUM(ticks.pitches)
        FROM ticks
        INNER JOIN climbs ON ticks.climb = climbs.id
        INNER JOIN climbed_partners ON ticks.climbed_id = climbed_with.climbing_id
        JOIN climbed_with ON climbed_partners.id = climbed_with.climbing_id
        JOIN partners ON climbed_with.partner_id = partners.id
        WHERE partners.id = {partner}
    """)

    for item in res:
        return item[0] 

def height_func(cur: Cursor, partner: int) -> int:
    res = cur.execute(f"""
        SELECT
            printf('%,d', SUM(ticks.height))
        FROM ticks
        INNER JOIN climbs ON ticks.climb = climbs.id
        INNER JOIN climbed_partners ON ticks.climbed_id = climbed_with.climbing_id
        JOIN climbed_with ON climbed_partners.id = climbed_with.climbing_id
        JOIN partners ON climbed_with.partner_id = partners.id
        WHERE partners.id = {partner}
    """)

    for item in res:
        return item[0] 

con = sqlite3.connect("ticks")
cur = con.cursor()

partners = partner_list()

# env = Environment(loader = FileSystemLoader('../websitejazzhands/templates'))
env = Environment(loader = FileSystemLoader('templates'))

template = env.get_template('partner_data.jinja')

for partner in partners:
    areas = area_func(cur, partner[0])
    days = days_func(cur, partner[0])
    pitches = pitches_func(cur, partner[0])
    height = height_func(cur, partner[0])
    if not os.path.exists(f"../websitejazzhands/climbing/partners/{partner[1]}-{partner[2]}"):
        os.makedirs(f"../websitejazzhands/climbing/partners/{partner[1]}-{partner[2]}")
    with open(f'../websitejazzhands/climbing/partners/{partner[1]}-{partner[2]}/index.html', 'w+') as f:
        print(template.render(
            partner_name = f"{partner[1]} {partner[2]}",
            area_count = f"{areas}",
            day_count = f"{days}",
            pitch_count = f"{pitches}",
            height_count = f"{height}"
        ), file = f)