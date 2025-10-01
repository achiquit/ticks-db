SELECT
    COUNT(ticks.id) AS 'Laps',
    climbs.name AS 'Climb',
    areas.area_name AS 'Area',
    (
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
            END
    ) AS 'Difficulty',
    SUM(CASE WHEN guided_id = -1 THEN 1 ELSE 0 END) AS 'Leisure Laps',
    SUM(CASE WHEN guided_id != -1 THEN 1 ELSE 0 END) AS 'Guiding Laps'
FROM
    ticks
INNER JOIN
    climbs ON ticks.climb = climbs.id,
    areas ON climbs.area = areas.id
GROUP BY climbs.id
ORDER BY laps DESC;