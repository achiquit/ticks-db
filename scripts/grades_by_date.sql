SELECT
    ticks.date,
    grades.grade
FROM
    ticks
    JOIN climbs ON climbs.id = ticks.climb
    JOIN join_grades ON join_grades.id = climbs.grade
    JOIN which_grades ON which_grades.id = join_grades.id
    JOIN grades ON grades.id = which_grades.grade;