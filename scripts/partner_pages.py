import sqlite3
from sqlite3 import Cursor
from jinja2 import Environment, FileSystemLoader
import os
import geopandas as gpd
import plotly.express as px
import plotly.io as pio

emerald = '#00d492'
dark_emerald = '#007a55'
bg_black = '#030712'

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

def heatmap_func(cur: Cursor, partner: int) -> None:
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

    geo_df = res

    fig = px.density_map(geo_df,
        lat=6,
        lon=7,
        z=5,
        radius=8,
        center=dict(lat=33, lon=320), zoom=1.4,
        map_style="carto-darkmatter",
        # hover_data=dict(
        #     Latitude=False,
        #     Longitude=False,
        #     Climb=True,
        #     Difficulty=True,
        #     Type=True,
        #     Height=True,
        #     Area=True
        # ),
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

    if not os.path.exists(f"../websitejazzhands/climbing/partners/{partner_name}"):
        os.makedirs(f"../websitejazzhands/climbing/partners/{partner_name}")
    pio.write_html(fig, f'../websitejazzhands/climbing/partners/{partner_name}/climb-locs.html', include_plotlyjs='cdn', config=config)

con = sqlite3.connect("ticks")
cur = con.cursor()

partners = partner_list()

# env = Environment(loader = FileSystemLoader('../websitejazzhands/templates'))
env = Environment(loader = FileSystemLoader('templates'))

template = env.get_template('partner_data.jinja')

for partner in partners:
    partner_id = partner[0]
    partner_name = f"{partner[1]}-{partner[2]}"
    areas = area_func(cur, partner_id)
    days = days_func(cur, partner_id)
    pitches = pitches_func(cur, partner_id)
    height = height_func(cur, partner_id)
    heatmap_func(cur, partner_id)
    if not os.path.exists(f"../websitejazzhands/climbing/partners/{partner_name}"):
        os.makedirs(f"../websitejazzhands/climbing/partners/{partner_name}")
    with open(f'../websitejazzhands/climbing/partners/{partner_name}/index.html', 'w+') as f:
        print(template.render(
            partner_name = f"{partner[1]} {partner[2]}",
            area_count = f"{areas}",
            day_count = f"{days}",
            pitch_count = f"{pitches}",
            height_count = f"{height}"
        ), file = f)