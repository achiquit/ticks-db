SELECT
    date AS 'Date',
    climbs.name AS 'Climb',
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
    (SELECT group_concat(climb_type.type, ', ')
        FROM join_types
        INNER JOIN which_types ON which_types.id = join_types.id
        INNER JOIN climb_type ON climb_type.id = which_types.type
        WHERE join_types.id = climbs.type) AS 'Type',
    areas.area_name AS 'Area',
    ticks.height AS 'Height',
    SUBSTR(gps, 1, INSTR(gps, ', ') - 1) AS 'Latitude',
    SUBSTRING(gps, INSTR(gps, ', ') + 1) AS 'Longitude'
FROM TICKS
INNER JOIN climbs ON climbs.id = ticks.climb
INNER JOIN areas ON climbs.area = areas.id
ORDER BY date DESC;