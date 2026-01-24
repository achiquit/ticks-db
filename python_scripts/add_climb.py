import sqlite3

con = sqlite3.connect("ticks-test")
cur = con.cursor()

data = []

res = cur.execute("SELECT id FROM climbs ORDER BY id DESC;")
last_climb = res.fetchone()
print(last_climb)

# name = input("Climb Name: ")

# grade = input("Grade: ")
# res = cur.execute("SELECT * FROM join_grades WHERE notes LIKE '%" + grade + "%';")
# print(res.fetchall())
# grade = input("Grade ID: ")

# danger = input("Danger Rating (-1, G, PG, PG-13, R, X): ")

# type = input("Climb Type (2: Boulder | 3: TR | 4: Sport | 5: Trad | h: help): ")
# if type == 'h':
#     res = cur.execute("SELECT * FROM climb_type;")
#     print(res.fetchall())

#     type = input("Climb Type: ")

# commitment = input("Commitment (I, II, etc): ")

# gps = input("GPS: ")

# area = input("Area: ")
# res = cur.execute("SELECT * FROM areas WHERE area_name LIKE '%" + area + "%';")
# print(res.fetchall())
# area = input("Area ID: ")

# notes = input("Notes: ")

# print(f"{name}, {grade}, {danger}, {type}, {commitment}, {gps}, {area}, {notes}")

# id = 676
# name = 'Pancho VIGGO Dies Again'
# grade = 20
# danger = -1
# type = 4
# commitment = -1
# gps = '25.94730, -100.47565'
# area = 141
# notes = 'Ayy'

# cur.execute(f"""
#     INSERT INTO climbs VALUES
#         ({id}, '{name}', {grade}, '{danger}', {type}, '{commitment}', '{gps}', {area}, '{notes}')
# """)
# con.commit()

# res = cur.execute("SELECT * FROM climbs ORDER BY id DESC LIMIT 2")
# print(res.fetchall ())