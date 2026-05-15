SELECT 
    DISTINCT(SUBSTR(gps, 1, INSTR(gps, ', ') - 1)) AS 'Latitude',
    SUBSTRING(gps, INSTR(gps, ', ') + 1) AS 'Longitude',
    name AS 'Climb',
    CASE
        WHEN climbs.danger IS -1 AND climbs.commitment IS -1 THEN
            (SELECT group_concat(grades.grade, ', ')
            FROM join_grades
            INNER JOIN which_grades ON which_grades.id = join_grades.id
            INNER JOIN grades ON grades.id = which_grades.grade
            WHERE join_grades.id = climbs.grade)
        WHEN climbs.danger IS NOT -1 AND climbs.commitment IS -1 THEN
            (SELECT group_concat(grades.grade, ', ') || ', ' || climbs.danger
            FROM join_grades
            INNER JOIN which_grades ON which_grades.id = join_grades.id
            INNER JOIN grades ON grades.id = which_grades.grade
            WHERE join_grades.id = climbs.grade)
        WHEN climbs.danger IS -1 AND climbs.commitment IS NOT -1 THEN
            (SELECT group_concat(grades.grade, ', ')  || ', Grade ' || climbs.commitment
            FROM join_grades
            INNER JOIN which_grades ON which_grades.id = join_grades.id
            INNER JOIN grades ON grades.id = which_grades.grade
            WHERE join_grades.id = climbs.grade)
        ELSE
            (SELECT group_concat(grades.grade, ', ') || ', ' || climbs.danger || ', Grade ' || climbs.commitment
            FROM join_grades
            INNER JOIN which_grades ON which_grades.id = join_grades.id
            INNER JOIN grades ON grades.id = which_grades.grade
            WHERE join_grades.id = climbs.grade)
        END AS 'Difficulty',
    areas.area_name AS 'Area',

    (SELECT group_concat(climb_type.type, ', ')
        FROM join_types
        INNER JOIN which_types ON which_types.id = join_types.id
        INNER JOIN climb_type ON climb_type.id = which_types.type
        WHERE join_types.id = climbs.type) AS 'Type'

    -- climb_type.type AS 'Type',

FROM
    climbs
    INNER JOIN areas ON areas.id = climbs.area

    -- INNER JOIN join_types ON climbs.type = join_types.id
    -- INNER JOIN which_types ON which_types.id = join_types.id
    -- INNER JOIN climb_type ON climb_type.id = which_types.type

WHERE gps != 'NULL';