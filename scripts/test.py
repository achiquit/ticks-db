import sqlite3
from pyhigh import get_elevation, clear_cache

con = sqlite3.connect("ticks")
cur = con.cursor()

res = cur.execute(f"""
    SELECT
        COUNT(*)
    FROM
        areas
    WHERE id = 152
    AND country = 'United States';
""")

for item in res:

    if item[0] == 1:
        elev = get_elevation(39.74437, -105.40297)
        elev = elev * 3.280839895
        elev = int(elev)
        print(elev)
    else:
        print("Oops, looks like this climb is international!")
        input("What's the elevation of the climb? : ")