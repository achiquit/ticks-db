import sqlite3
from sqlite3 import Cursor

con = sqlite3.connect("ticks")
cur = con.cursor()
listy = []

# Make a list of climb IDs
res = cur.execute(f"""
    SELECT id
    FROM climbs
""")

for item in res:
    listy += [list(item)]

# Add most common height to each climb ID
for climb in listy:
    res = cur.execute(f"""
        SELECT ticks.height
        FROM ticks
        INNER JOIN climbs ON ticks.climb = climbs.id
        WHERE climbs.id = {climb[0]}
        GROUP BY ticks.height
        ORDER BY COUNT(ticks.height)
        DESC LIMIT 1;
    """)
    for item in res:
        climb.append(item[0])

# Add height column to climbs table
res = cur.execute(f"""
    ALTER TABLE climbs ADD COLUMN height INTEGER;
""")

# Iterate through the list and add the most common height to the new height column in the climbs table
for climb in listy:
    res = cur.execute(f"""
        UPDATE climbs
        SET height = {climb[1]}
        WHERE id = {climb[0]}
    """)

con.commit()
    
res = cur.execute(f"""
    SELECT id, name, height
    FROM climbs
    ORDER BY id DESC
    LIMIT 5;
""")