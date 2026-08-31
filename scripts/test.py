import sqlite3
from datetime import datetime
import csv
import no_plus_minus

con = sqlite3.connect("ticks")
cur = con.cursor()

year = 2019
current_year = datetime.now().year

while year <= current_year:

    res = cur.execute(f"""
        SELECT
            grades.id AS 'ID',
            grades.grade AS 'Grade',
            0 AS 'Count',
            'NULL' as 'Type'
        FROM 
            grades
        WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE '5.10' AND grades.grade NOT LIKE '5.11' AND grades.grade NOT LIKE '5.12' AND grades.grade NOT LIKE '5.13' AND grades.grade NOT LIKE '5.14' AND grades.grade NOT LIKE '5.15'

        UNION

        SELECT
            grades.id AS 'ID',
            grades.grade AS 'Grade',
            COUNT(ticks.id) AS 'Count',
            'Sport' AS 'Type'
        FROM
            grades
            INNER JOIN which_grades ON which_grades.grade = grades.id
            INNER JOIN join_grades ON join_grades.id = which_grades.id
            LEFT JOIN climbs ON climbs.grade = join_grades.id
            LEFT JOIN ticks ON ticks.climb = climbs.id
        WHERE grades.grade LIKE '5.%' AND climbs.type = 4 AND ticks.date LIKE '%{year}%'
        GROUP BY grades.grade

        UNION

        SELECT
            grades.id AS 'ID',
            grades.grade AS 'Grade',
            COUNT(ticks.id) AS 'Count',
            'Trad' AS 'Type'
        FROM
            grades
            INNER JOIN which_grades ON which_grades.grade = grades.id
            INNER JOIN join_grades ON join_grades.id = which_grades.id
            LEFT JOIN climbs ON climbs.grade = join_grades.id
            LEFT JOIN ticks ON ticks.climb = climbs.id
        WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%' AND climbs.type = 5 AND ticks.date LIKE '%{year}%' OR climbs.type = 12 AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%' AND ticks.date LIKE '%{year}%' OR climbs.type = 13 AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%' AND ticks.date LIKE '%{year}%'
        GROUP BY grades.grade;
    """)

    res = res.fetchall()

    with open(f'test/grades_and_types_for_{year}.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(res)

    no_plus_minus.even_better_ver(f'test/grades_and_types_for_{year}.csv', 1, 2, [3])

    year += 1