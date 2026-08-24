###### ONLY WORKS FOR CLIMBS WITHIN THE UNITED STATES ########

import sqlite3
from pyhigh import get_elevation_batch, get_elevation, clear_cache

con = sqlite3.connect("ticks")
cur = con.cursor()

res = cur.execute("""
    SELECT 
        SUBSTRING(gps, 1, INSTR(gps, ',') - 1),
        SUBSTRING(gps, INSTR(gps, ',') + 2)
    FROM climbs
    INNER JOIN areas ON climbs.area = areas.id
    WHERE
        country = "United States";
""")

locs = []

for item in res:
    locs.append((float(item[0]), float(item[1])))

# for loc in locs:
#     print(f"Getting elev for {loc}")
#     elev = get_elevation(lat=loc[0], lon=loc[1])
#     print(elev)

# print(locs)
# print(type(locs[0]))

# locs_test = [(36.52011, -118.671), (36.62011, -118.771)]
# print(locs_test)
# print(type(locs_test[0]))

elevs = get_elevation_batch(locs)

elevs = sorted(elevs)

for elev in elevs:
    elev = elev * 3.280839895
    elev = int(elev)
    print(f"{elev}ft")

clear_cache()