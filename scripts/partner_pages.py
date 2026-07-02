import sqlite3
from sqlite3 import Cursor
from jinja2 import Environment, FileSystemLoader
import os
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import csv
import shutil

emerald = '#00d492'
dark_emerald = '#007a55'
bg_black = '#030712'

def partner_list(cur: Cursor) -> list:

    partners = []

    res = cur.execute(f"""
        SELECT
            id,
            fname,
            lname
        FROM
            partners
    """)

    for item in res:
        partners += [list(item)]
    
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

def heatmap_func(cur: Cursor, partner: int, partner_name_code: str) -> None:
    
    res = cur.execute(f"""
        SELECT
            date AS 'Date',
            climbs.name AS 'Climb',
            CASE
                WHEN climbs.danger IS -1 AND climbs.commitment IS -1 THEN
                    (SELECT group_concat(grades.grade, ', ')
                    FROM join_grades
                    INNER JOIN which_grades ON which_grades.id = join_grades.id
                    INNER JOIN grades ON grades.id = which_grades.grade
                    WHERE join_grades.id = climbs.grade)
                WHEN climbs.danger IS NOT -1 AND climbs.commitment IS -1 THEN
                    (SELECT group_concat(grades.grade, ', ') || ', ' || climbs.danger
                    FROM join_grades
                    INNER JOIN which_grades ON which_grades.id = join_grades.id
                    INNER JOIN grades ON grades.id = which_grades.grade
                    WHERE join_grades.id = climbs.grade)
                WHEN climbs.danger IS -1 AND climbs.commitment IS NOT -1 THEN
                    (SELECT group_concat(grades.grade, ', ')  || ', Grade ' || climbs.commitment
                    FROM join_grades
                    INNER JOIN which_grades ON which_grades.id = join_grades.id
                    INNER JOIN grades ON grades.id = which_grades.grade
                    WHERE join_grades.id = climbs.grade)
                ELSE
                    (SELECT group_concat(grades.grade, ', ') || ', ' || climbs.danger || ', Grade ' || climbs.commitment
                    FROM join_grades
                    INNER JOIN which_grades ON which_grades.id = join_grades.id
                    INNER JOIN grades ON grades.id = which_grades.grade
                    WHERE join_grades.id = climbs.grade)
                END AS 'Difficulty',
            (SELECT group_concat(climb_type.type, ', ')
                FROM join_types
                INNER JOIN which_types ON which_types.id = join_types.id
                INNER JOIN climb_type ON climb_type.id = which_types.type
                WHERE join_types.id = climbs.type) AS 'Type',
            areas.area_name AS 'Area',
            ticks.height AS 'Height',
            SUBSTR(gps, 1, INSTR(gps, ', ') - 1) AS 'Latitude',
            SUBSTRING(gps, INSTR(gps, ', ') + 1) AS 'Longitude'
        FROM TICKS
        INNER JOIN climbs ON climbs.id = ticks.climb
        INNER JOIN areas ON climbs.area = areas.id
        INNER JOIN climbed_partners ON ticks.climbed_id = climbed_with.climbing_id
        JOIN climbed_with ON climbed_partners.id = climbed_with.climbing_id
        JOIN partners ON climbed_with.partner_id = partners.id
        WHERE partners.id = {partner}
        ORDER BY date DESC;
    """)

    with open(f'../websitejazzhands/climbing/partners/{partner_name_code}/climb-locs.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Climb', 'Difficulty', 'Type', 'Area', 'Height', 'Latitude', 'Longitude'])
        writer.writerows(res)

    geo_df = gpd.read_file(f"""../websitejazzhands/climbing/partners/{partner_name_code}/climb-locs.csv""")

    os.remove(f"""../websitejazzhands/climbing/partners/{partner_name_code}/climb-locs.csv""")

    fig = px.density_map(geo_df,
        lat='Latitude',
        lon='Longitude',
        z='Height',
        radius=8,
        center=dict(lat=33, lon=320), zoom=1.4,
        map_style="carto-darkmatter",
        hover_data=dict(
            Latitude=False,
            Longitude=False,
            Climb=True,
            Difficulty=True,
            Type=True,
            Height=True,
            Area=True
        ),
        color_continuous_scale=["#ff2b6d", "#9810fa", emerald],
        range_color=[0,20000]
    )

    hover_data=dict(
            Latitude=False,
            Longitude=False,
            Climb=True,
            Difficulty=True,
            Type=True
        ),

    fig.update_layout(
        plot_bgcolor=bg_black,
        paper_bgcolor=bg_black,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    config = {
        'scrollZoom': True,
        'displaylogo': False,
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['select', 'lasso', 'pan', 'toImage']
    }

    pio.write_html(fig, f'../websitejazzhands/climbing/partners/{partner_name_code}/climb-locs.html', include_plotlyjs='cdn', config=config)

def all_ticks(cur: Cursor, partner: int, partner_name_code) -> None:
    res = cur.execute(f"""
        SELECT 
            ticks.date AS 'Date', 
            climbs.name AS 'Climb', 
            (
                CASE
                    WHEN climbs.danger IS -1 AND climbs.commitment IS -1 THEN
                        (SELECT group_concat(grades.grade, ', ')
                        FROM join_grades
                        INNER JOIN which_grades ON which_grades.id = join_grades.id
                        INNER JOIN grades ON grades.id = which_grades.grade
                        WHERE join_grades.id = climbs.grade)
                    WHEN climbs.danger IS NOT -1 AND climbs.commitment IS -1 THEN
                        (SELECT group_concat(grades.grade, ', ') || ', ' || climbs.danger
                        FROM join_grades
                        INNER JOIN which_grades ON which_grades.id = join_grades.id
                        INNER JOIN grades ON grades.id = which_grades.grade
                        WHERE join_grades.id = climbs.grade)
                    WHEN climbs.danger IS -1 AND climbs.commitment IS NOT -1 THEN
                        (SELECT group_concat(grades.grade, ', ')  || ', Grade ' || climbs.commitment
                        FROM join_grades
                        INNER JOIN which_grades ON which_grades.id = join_grades.id
                        INNER JOIN grades ON grades.id = which_grades.grade
                        WHERE join_grades.id = climbs.grade)
                    ELSE
                        (SELECT group_concat(grades.grade, ', ') || ', ' || climbs.danger || ', Grade ' || climbs.commitment
                        FROM join_grades
                        INNER JOIN which_grades ON which_grades.id = join_grades.id
                        INNER JOIN grades ON grades.id = which_grades.grade
                        WHERE join_grades.id = climbs.grade)
                    END
            ) AS 'Difficulty',
            (
                SELECT group_concat(climb_type.type, ', ')
                FROM join_types
                INNER JOIN which_types ON which_types.id = join_types.id
                INNER JOIN climb_type ON climb_type.id = which_types.type
                WHERE join_types.id = climbs.type
            ) AS 'Type',
            areas.area_name AS 'Area',
            ticks.pitches AS 'Pitches',
            ticks.height AS 'Height',
            ticks.style || ', ' || ticks.success AS 'Style',
            group_concat(partners.fname || ' ' || substr(partners.lname, 1, 2) || '.', ', ') AS 'Partner(s)',
            CASE
                WHEN ticks.notes IS -1 THEN 'Nuthin'' to say'
                ELSE ticks.notes 
            END AS 'Notes'
        FROM
            ticks
            INNER JOIN climbs ON ticks.climb = climbs.id
            INNER JOIN areas ON areas.id = climbs.area
            INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
            INNER JOIN climbed_with ON climbed_with.climbing_id = climbed_partners.id
            INNER JOIN partners ON partners.id = climbed_with.partner_id
        GROUP BY ticks.id
        HAVING ',' || group_concat(partners.id) || ',' LIKE '%,{partner},%'
        ORDER BY 
            date DESC,
            ticks.id DESC
        LIMIT 1000000000;
    """)

    if not os.path.exists(f"../websitejazzhands/climbing/partners/{partner_name_code}/data"):
        os.makedirs(f"../websitejazzhands/climbing/partners/{partner_name_code}/data")
    with open(f'../websitejazzhands/climbing/partners/{partner_name_code}/data/all-ticks.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Climb', 'Difficulty', 'Type', 'Area', 'Pitches', 'Height', 'Style', 'Partner(s)', 'Notes'])
        writer.writerows(res)

    # Source path
    src = r'../websitejazzhands/climbing/js'

    # Destination pat
    dest = f'../websitejazzhands/climbing/partners/{partner_name_code}/js'

    # Copy the content of source to destination
    try:
        shutil.copytree(src, dest)
    except:
        pass

def top_areas(cur: Cursor, partner: int, partner_name_code) -> None:
    res = cur.execute(f"""
        SELECT
            areas.area_name AS 'Area',
            COUNT(DISTINCT ticks.date) AS 'Days',
            SUM(ticks.height) AS 'Height',
            areas.state || ', ' || areas.country AS 'Location'
        FROM
            ticks
            INNER JOIN climbs ON ticks.climb = climbs.id
            INNER JOIN areas ON areas.id = climbs.area
            INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
            INNER JOIN climbed_with ON climbed_with.climbing_id = climbed_partners.id
            INNER JOIN partners ON partners.id = climbed_with.partner_id
        GROUP BY areas.area_name, partners.id
        HAVING ',' || group_concat(partners.id) || ',' LIKE '%,{partner},%'
        ORDER BY SUM(ticks.height) ASC;
    """)

    if not os.path.exists(f"../websitejazzhands/climbing/partners/{partner_name_code}/data"):
        os.makedirs(f"../websitejazzhands/climbing/partners/{partner_name_code}/data")
    with open(f'../websitejazzhands/climbing/partners/{partner_name_code}/data/top-areas.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Area', 'Days', 'Height', 'Location'])
        writer.writerows(res)

def update_all() -> None:
    con = sqlite3.connect("ticks")
    cur = con.cursor()

    env = Environment(loader = FileSystemLoader('templates'))

    partners = partner_list(cur)

    for partner in partners:
        partner_id = partner[0]

        partner_name_code = f"{partner[1]}-{partner[2]}"
        if not os.path.exists(f"../websitejazzhands/climbing/partners/{partner_name_code}"):
            os.makedirs(f"../websitejazzhands/climbing/partners/{partner_name_code}")
        areas = area_func(cur, partner_id)
        days = days_func(cur, partner_id)
        pitches = pitches_func(cur, partner_id)
        height = height_func(cur, partner_id)
        heatmap_func(cur, partner_id, partner_name_code)
        all_ticks(cur, partner_id, partner_name_code)
        top_areas(cur, partner_id, partner_name_code)

        template = env.get_template('partner_data.jinja')

        with open(f'../websitejazzhands/climbing/partners/{partner_name_code}/index.html', 'w+') as f:
            print(template.render(
                partner_name_read = f"{partner[1]} {partner[2]}",
                partner_name_code = f"{partner_name_code}",
                area_count = f"{areas}",
                day_count = f"{days}",
                pitch_count = f"{pitches}",
                height_count = f"{height}"
            ), file = f)

        template = env.get_template('ticks.jinja')
        with open(f'../websitejazzhands/climbing/partners/{partner_name_code}/ticks.html', 'w+') as f:
            print(template.render(
                partner_name_code = f"{partner_name_code}"
            ), file = f)

        template = env.get_template('top_areas.jinja')
        with open(f'../websitejazzhands/climbing/partners/{partner_name_code}/top_areas.html', 'w+') as f:
            print(template.render(
                partner_name_code = f"{partner_name_code}"
            ), file = f)

def main(partners_to_update: list):   
    con = sqlite3.connect("ticks")
    cur = con.cursor()

    partners = partner_list(cur)

    env = Environment(loader = FileSystemLoader('templates'))

    for partner in partners:
        partner_id = partner[0]

        for to_update in partners_to_update:
            if partner_id == to_update:

                partner_name_code = f"{partner[1]}-{partner[2]}"
                if not os.path.exists(f"../websitejazzhands/climbing/partners/{partner_name_code}"):
                    os.makedirs(f"../websitejazzhands/climbing/partners/{partner_name_code}")
                areas = area_func(cur, partner_id)
                days = days_func(cur, partner_id)
                pitches = pitches_func(cur, partner_id)
                height = height_func(cur, partner_id)
                heatmap_func(cur, partner_id, partner_name_code)
                all_ticks(cur, partner_id, partner_name_code)
                top_areas(cur, partner_id, partner_name_code)
                
                template = env.get_template('partner_data.jinja')

                with open(f'../websitejazzhands/climbing/partners/{partner_name_code}/index.html', 'w+') as f:
                    print(template.render(
                        partner_name_read = f"{partner[1]} {partner[2]}",
                        partner_name_code = f"{partner_name_code}",
                        area_count = f"{areas}",
                        day_count = f"{days}",
                        pitch_count = f"{pitches}",
                        height_count = f"{height}"
                    ), file = f)
                
                template = env.get_template('ticks.jinja')
                with open(f'../websitejazzhands/climbing/partners/{partner_name_code}/ticks.html', 'w+') as f:
                    print(template.render(
                        partner_name_code = f"{partner_name_code}"
                    ), file = f)
                
                template = env.get_template('top_areas.jinja')
                with open(f'../websitejazzhands/climbing/partners/{partner_name_code}/top_areas.html', 'w+') as f:
                    print(template.render(
                        partner_name_code = f"{partner_name_code}"
                    ), file = f)

if __name__ == '__main__':
    update_all()