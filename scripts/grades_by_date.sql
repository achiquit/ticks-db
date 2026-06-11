SELECT
    ticks.date,
    grades.grade,
    climbs.name,
    climb_type.type
FROM
    ticks
    JOIN climbs ON climbs.id = ticks.climb
    JOIN join_grades ON join_grades.id = climbs.grade
    JOIN which_grades ON which_grades.id = join_grades.id
    JOIN grades ON grades.id = which_grades.grade
    JOIN join_types ON join_types.id = climbs.type
    JOIN which_types ON which_types.id = join_types.id
    JOIN climb_type ON climb_type.id = which_types.type
WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%' AND climb_type.type NOT LIKE 'TR' AND climb_type.type NOT LIKE 'Aid' AND ticks.success = 'Redpoint' OR grades.grade LIKE '5.%' AND grades.grade NOT LIKE 'C%' AND grades.grade NOT LIKE '%Snow%' AND grades.grade NOT LIKE '%th%' AND climb_type.type NOT LIKE 'TR' AND climb_type.type NOT LIKE 'Aid' AND ticks.success = 'Onsight';