SELECT 
    ticks.date AS 'Date', 
    climbs.name AS 'Climb', 
    (
        CASE
            WHEN climbs.commitment IS -1 THEN
                (SELECT group_concat(grades.grade, ', ')
                FROM join_grades
                INNER JOIN which_grades ON which_grades.id = join_grades.id
                INNER JOIN grades ON grades.id = which_grades.grade
                WHERE join_grades.id = climbs.grade)
            ELSE
                (SELECT group_concat(grades.grade, ', ')  || ', Grade ' || climbs.commitment
                FROM join_grades
                INNER JOIN which_grades ON which_grades.id = join_grades.id
                INNER JOIN grades ON grades.id = which_grades.grade
                WHERE join_grades.id = climbs.grade)
            END
    ) AS 'Difficulty',
    (
        SELECT group_concat(climb_type.type, ', ')
        FROM join_types
        INNER JOIN which_types ON which_types.id = join_types.id
        INNER JOIN climb_type ON climb_type.id = which_types.type
        WHERE join_types.id = climbs.type
    ) AS 'Type',
    areas.area_name AS 'Area',
    ticks.pitches AS 'Pitches',
    ticks.height AS 'Height',
    ticks.style AS 'Style',
    CASE
        WHEN climbed_id IS -1 AND guided_id IS -1 THEN 'Unknown Partner'
        WHEN climbed_id IS -1 THEN 'Guiding'
        ELSE
        (
            SELECT group_concat(partners.fname || ' ' || partners.lname, ', ')
            FROM climbed_partners
            INNER JOIN climbed_with ON climbed_with.climbing_id = climbed_partners.id
            INNER JOIN partners ON partners.id = climbed_with.partner_id
            WHERE climbed_partners.id = ticks.climbed_id
        ) END AS 'Partner(s)',
    CASE
        WHEN ticks.notes IS -1 THEN 'Nuthin'' to say'
        ELSE ticks.notes 
    END AS 'Notes'
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN areas ON areas.id = climbs.area
GROUP BY ticks.id
ORDER BY date DESC
LIMIT 1000000000;