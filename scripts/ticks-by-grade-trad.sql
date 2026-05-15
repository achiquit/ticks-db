SELECT
    DISTINCT grades.grade AS 'Grade',
    COUNT(ticks.id) AS 'Count',
    'Sport' AS 'Type'
FROM
    grades
    INNER JOIN which_grades ON which_grades.grade = grades.id
    INNER JOIN join_grades ON join_grades.id = which_grades.id
    LEFT JOIN climbs ON climbs.grade = join_grades.id
    LEFT JOIN ticks ON ticks.climb = climbs.id
WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE '5.10' AND grades.grade NOT LIKE '5.11' AND grades.grade NOT LIKE '5.12' AND grades.grade NOT LIKE '5.13' AND grades.grade NOT LIKE '5.14' AND grades.grade NOT LIKE '5.15' AND climbs.type IN [5, 12, 13]
GROUP BY grades.grade
ORDER BY grades.id ASC;

-- trad: 5, 12, 13
-- sport: 4