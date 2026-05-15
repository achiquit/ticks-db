SELECT
    grades.grade AS 'Grade',
    0 AS 'Count'
FROM 
    grades
WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE '5.10' AND grades.grade NOT LIKE '5.11' AND grades.grade NOT LIKE '5.12' AND grades.grade NOT LIKE '5.13' AND grades.grade NOT LIKE '5.14' AND grades.grade NOT LIKE '5.15'