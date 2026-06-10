SELECT
    ticks.date,
    grades.grade
FROM
    ticks
    JOIN climbs ON climbs.id = ticks.climb
    JOIN join_grades ON join_grades.id = climbs.grade
    JOIN which_grades ON which_grades.id = join_grades.id
    JOIN grades ON grades.id = which_grades.grade
WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%' AND climbs.type = 5 OR climbs.type = 12 AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%' OR climbs.type = 13 AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%';