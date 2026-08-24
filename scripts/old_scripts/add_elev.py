##### Retroactively adding elevation to all the climbs I've already done #######

import os
import shutil
import sqlite3
from pyhigh import get_elevation, clear_cache

if os.path.exists("ticks-elev"):
    os.remove("ticks-elev")
    shutil.copyfile("ticks", "ticks-elev")

con = sqlite3.connect("ticks-elev")
cur = con.cursor()

res = cur.execute("""
    ALTER TABLE
        climbs
    ADD COLUMN
        elevation 
""")

res = cur.execute("""
    SELECT 
        climbs.id,
        SUBSTRING(gps, 1, INSTR(gps, ',') - 1),
        SUBSTRING(gps, INSTR(gps, ',') + 2)
    FROM climbs
    INNER JOIN areas ON climbs.area = areas.id
    WHERE
        country = "United States";
""")

locs = []

for item in res:
    locs.append([int(item[0]), (float(item[1]), float(item[2]))])

for item in locs:
    print(item)

locs_with_elevs = []

for item in locs:
    elev = get_elevation(lat=item[1][0], lon=item[1][1])
    elev = elev * 3.280839895
    elev = int(elev)
    locs_with_elevs.append([item[0], elev])

for item in locs_with_elevs:
    print(item)

for item in locs_with_elevs:
    res = cur.execute(f"""
        UPDATE
            climbs
        SET
            elevation = {item[1]}
        WHERE
            id = {item[0]}
    """)

res = cur.execute("""
    SELECT 
        climbs.id,
        SUBSTRING(gps, 1, INSTR(gps, ',') - 1),
        SUBSTRING(gps, INSTR(gps, ',') + 2),
        elevation
    FROM climbs
    INNER JOIN areas ON climbs.area = areas.id;
""")

for item in res:
    print(item)

int_climbs = [[169, 7377],[187, 820],[188, 820],[189, 820],[190, 820],[191, 282],[192, 282],[193, 260],[194, 400],[195, 400],[196, 282],[197, 237],[198, 97],[199, 97],[200, 97],[201, 1275],[202, 1275],[203, 1161],[204, 1161],[205, 1161],[206, 1161],[207, 1161],[208, 1161],[209, 1161],[210, 6637],[211, 388],[212, 75],[213, 75],[214, 75],[215, 75],[216, 75],[217, 75],[218, 102],[219, 160],[220, 102],[221, 102],[552, 34],[553, 630],[554, 491],[555, 630],[556, 1934],[557, 1934],[558, 6168],[559, 34],[560, 266],[561, 266],[562, 266],[563, 266],[564, 266],[565, 266],[566, 2380],[567, 488],[568, 488],[569, 591],[570, 591],[571, 318],[654, 2610],[655, 2432],[656, 2326],[657, 2324],[658, 2282],[659, 2306],[660, 2301],[661, 2306],[662, 2380],[663, 2296],[664, 2294],[665, 2314],[666, 2652],[667, 2545],[668, 2483],[669, 3224],[670, 2310],[671, 2927],[672, 3014],[673, 2343],[674, 2453],[683, 935],[684, 999],[685, 1000],[686, 1000],[687, 827],[688, 1508],[689, 1508],[690, 834],[691, 861]]

for climb in int_climbs:
    res = cur.execute(f"""
        UPDATE
            climbs
        SET
            elevation = {climb[1]}
        WHERE
            id = {climb[0]}
    """)
    con.commit()

# con.commit()