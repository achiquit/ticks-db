import sqlite3
import csv

def magic():

    # Open DB
    con = sqlite3.connect("ticks")
    cur = con.cursor()
    import numpy as np

    # Read in sqlite script
    with open('scripts/ticks-by-grade.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    res = cur.execute(sql_script)
    ticks_by_grade = res.fetchall()
    ticks_by_grade = list(ticks_by_grade)
    ticks_by_grade = np.array(ticks_by_grade).tolist()

    for item in ticks_by_grade:
        item[0] = int(item[0])
        item[2] = int(item[2])

    # Remove all NULL category entries (I know having four of these is dumb, but having one misses a ton of NULL categories, and setting up a recursive script somehow removes everything? Idk man, if it ain't broke don't fix it.)
    # for entry in ticks_by_grade:
    #     if entry[3] == 'NULL':
    #         ticks_by_grade.remove(entry)
    # for entry in ticks_by_grade:
    #     if entry[3] == 'NULL':
    #         ticks_by_grade.remove(entry)
    # for entry in ticks_by_grade:
    #     if entry[3] == 'NULL':
    #         ticks_by_grade.remove(entry)
    # for entry in ticks_by_grade:
    #     if entry[3] == 'NULL':
    #         ticks_by_grade.remove(entry)

    to_remove = []
    for entry in ticks_by_grade:
        if "+" in entry[1]:
            to_remove.append(entry)
        elif "-" in entry[1]:
            to_remove.append(entry)

    for item in to_remove:
        added = False
        while added == False:
            for grade in ticks_by_grade:
                if item[3] == grade[3]:
                    if str(item[1][0:3]) == str(grade[1][0:3]):
                        if len(grade[1]) == 3:
                            grade[2] += item[2]
                            added = True
        ticks_by_grade.remove(item)

    ticks_by_grade.insert(0, ['ID', 'Grade', 'Count', 'Type'])

    with open('data/ticks-by-grade.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(ticks_by_grade)

if __name__ == '__main__':
    magic()