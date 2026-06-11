import sqlite3
import csv

def main(sql_path: str, csv_path: str, int_conv = bool):

    # Open DB
    con = sqlite3.connect("ticks")
    cur = con.cursor()
    import numpy as np

    # Read in sqlite script
    with open(sql_path, 'r') as sql_file:
        sql_script = sql_file.read()

    res = cur.execute(sql_script)
    ticks_by_grade = res.fetchall()
    ticks_by_grade = list(ticks_by_grade)
    ticks_by_grade = np.array(ticks_by_grade).tolist()

    to_remove = []
    for entry in ticks_by_grade:
        if "+" in entry[1]:
            if int_conv is True:
                to_remove.append(entry)
            else:
                entry[1] = entry[1][0:3]
        elif "-" in entry[1]:
            if int_conv is True:
                to_remove.append(entry)
            else:
                entry[1] = entry[1][0:3]

    if int_conv is True:
        for item in ticks_by_grade:
            item[0] = int(item[0])
            item[2] = int(item[2])

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
    else:
        ticks_by_grade.insert(0, ['Date', 'Grade', 'Climb', 'Type'])

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(ticks_by_grade)

if __name__ == '__main__':
    main()