SELECT
    ticks.date,
    grades.grade,
    types.type
FROM
    ticks
    JOIN climbs ON climbs.id = ticks.climb
    JOIN join_grades ON join_grades.id = climbs.grade
    JOIN which_grades ON which_grades.id = join_grades.id
    JOIN grades ON grades.id = which_grades.grade
    JOIN join_types ON join_types.id = climbs.type
    JOIN which_types ON which_types.id = join_types.id
    JOIN types ON types.id = join_types.type
WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%' AND climbs.type = 5 OR climbs.type = 12 AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%' OR climbs.type = 13 AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%';