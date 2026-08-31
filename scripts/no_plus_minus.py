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

def better_ver(csv_path: str, grade_pos: int, headers: list) -> None:

    table = []

    with open(csv_path,'r') as data:
        for line in csv.reader(data):
            table.append(line)

    table.remove(table[0])

    for line in table:
        count = line[2]
        line[2] = int(count)

    to_remove = []
    for entry in table:
        if "+" in entry[grade_pos]:
            to_remove.append(entry)
        elif "-" in entry[grade_pos]:
            to_remove.append(entry)

    for item in to_remove:
        table.remove(item)

    for item_remove in to_remove:
        added = False
        while added == False:
            for item in table:
                if f"{item_remove[grade_pos][0:3]}{item_remove[3]}{item_remove[4]}" == f"{item[grade_pos][0:3]}{item[3]}{item[4]}":
                    item[2] += item_remove[2]
                    added = True

    table.insert(0, headers)

    with open(csv_path, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table)

def even_better_ver(csv_path: str, grade_pos: int, count_pos: int, other_factors: list, add_header: bool = False, header: list = [], int_conv: bool = True, remove_0: bool = True, remove_5_point_1: bool = True) -> None:

    # Args explained:
    #   csv_path: Path to the csv with the data
    #   grade_pos: Where the grade names are stored
    #   count_pos: Where the counts are stored
    #   other_factors: Position of other factors like Sport/Trad, Success, etc.
    #   add_header: Defaults to false, determines whether the user wants to add a header to the data
    #   header: If add_header is true, this is the new header
    #   int_conv: Defaults to true, converts count to int. Idk if I'll ever want this to be false, but it can be!
    #   remove_0: Defaults to true, removes any items with a 0 count
    #   remove_5_point_1: Defaults to true, removes any items with a grade 5.1; they're weird db noise I haven't fixed yet

    to_remove = []

    with open(csv_path, 'r') as f:
        csv_reader = csv.reader(f)
        ticks_count = list(csv_reader)

    if int_conv is True:
        for item in ticks_count:
            item[count_pos] = int(item[count_pos])

    # Go through and find all the grades with a + or a -, take them out of the original list and add them to their own list
    found = 1
    while found > 0:
        found = 0
        for item in ticks_count:
            if "+" in item[grade_pos]:
                found += 1
                item[grade_pos] = item[grade_pos][0:3]
                to_remove.append(item)
                ticks_count.remove(item)
            elif "-" in item[grade_pos]:
                found += 1
                item[grade_pos] = item[grade_pos][0:3]
                to_remove.append(item)
                ticks_count.remove(item)

    # Remove any redundant grades accounting for other factors - MAY ENCOUNTER FACTOR RELATED BUGS HERE
    count = 0
    while count < len(ticks_count) - 1:
        if ticks_count[count][grade_pos] == ticks_count[count + 1][grade_pos]:
            if ticks_count[count][count_pos] == 0:
                ticks_count.remove(ticks_count[count])
            elif ticks_count[count + 1][count_pos] == 0:
                ticks_count.remove(ticks_count[count + 1])
                count -= 1
        count += 1

    # Add all the counts of all the grades with a + or - to their corresponding grades, accounting for other factors 
    for item in to_remove:
        added = False
        while added is False:
            for grade in ticks_count:
                if item[grade_pos] == grade[grade_pos]:
                    if len(other_factors) > 0:
                        factor = 0
                        factor_status = []
                        while factor < len(other_factors):
                            if item[other_factors[factor]] == grade[other_factors[factor]]:
                                factor_status.append(True)
                            else:
                                factor_status.append(False)
                            factor += 1
                        if False not in factor_status:
                            grade[count_pos] += item[count_pos]
                        added = True
                    else:
                        grade[count_pos] += item[count_pos]
                        added = True

    # remove any rows with a 0 count
    found = 1
    while found > 0:
        found = 0
        for item in ticks_count:
            if item[count_pos] == 0:
                ticks_count.remove(item)
                found += 1

    # remove any rows where the grade is 5.1
    found = 1
    while found > 0:
        found = 0
        for item in ticks_count:
            if item[grade_pos] == '5.1':
                ticks_count.remove(item)
                found += 1

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if add_header is True:
            if len(header) == len(ticks_count[0]):
                writer.writerow(header)  
            else:
                print("It didn't work because the header you're trying to add doesn't have the same number of columns as the data you're using dawg!")
                
        writer.writerows(ticks_count)

if __name__ == '__main__':
    main()