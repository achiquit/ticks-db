-- Original query below

-- SELECT ticks.id AS tick_id, ticks.date AS tick_date, climbs.name AS climb_name, grades.grade AS grade, areas.area_name AS area, ticks.pitches AS pitches, ticks.height || 'ft' AS height, ticks.style || ', ' || ticks.success AS style, 
-- CASE 
--     WHEN climbed_id IS -1 AND guided_id IS -1 THEN 'Unknown Partner'
--     WHEN climbed_id IS -1 THEN 'Guiding'
--     ELSE partners.fname || ' ' || partners.lname 
--     END AS pal, 
-- CASE
--     WHEN ticks.notes IS -1 THEN 'Nuthin'' to say' 
--     ELSE ticks.notes
--     END AS notes
-- FROM
--     ticks
--     INNER JOIN climbs ON ticks.climb = climbs.id
--     INNER JOIN areas ON climbs.area = areas.id
--     INNER JOIN join_grades ON climbs.grade = join_grades.id
--     FULL OUTER JOIN which_grades ON join_grades.id = which_grades.id
--     FULL OUTER JOIN grades ON which_grades.grade = grades.grade
--     INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
--     FULL OUTER JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
--     FULL OUTER JOIN partners ON climbed_with.partner_id = partners.id
-- ORDER BY ticks.id DESC
-- LIMIT 5;

-- Further isolating below
SELECT name AS 'Name', area AS 'Area', group_concat(grade, ', ') AS 'Grade', notes AS 'Notes'
FROM (
    SELECT climbs.id AS id, areas.area_name AS area, climbs.name AS name, grades.grade AS grade, climbs.notes AS notes
    FROM
        climbs
        INNER JOIN areas ON climbs.area = areas.id
        INNER JOIN join_grades ON climbs.grade = join_grades.id
        FULL OUTER JOIN which_grades ON join_grades.id = which_grades.id
        LEFT JOIN grades ON which_grades.grade = grades.id
        INNER JOIN join_types ON climbs.type = join_types.id
        FULL OUTER JOIN which_types ON join_types.id = which_types.id
        LEFT JOIN climb_type ON which_types.type = climb_type.id
    ORDER BY climbs.id DESC
    LIMIT 5
)
-- GROUP BY id
ORDER BY id DESC
LIMIT 5;