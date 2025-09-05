SELECT tick_date AS 'Date', climb_name AS 'Climb', grade AS 'Grade', type AS 'Type', area AS 'Area', pitches AS 'Pitches', height as 'Height', style AS 'Style', group_concat(pal, ', ') AS 'Partner(s)', notes AS 'Notes'
FROM (
    SELECT ticks.id AS tick_id, ticks.date AS tick_date, climbs.name AS climb_name, grades.grade AS grade, climb_type.type AS type, areas.area_name AS area, ticks.pitches AS pitches, ticks.height || 'ft' AS height, ticks.style || ', ' || ticks.success AS style, 
    CASE 
        WHEN climbed_id IS -1 AND guided_id IS -1 THEN 'Unknown Partner'
        WHEN climbed_id IS -1 THEN 'Guiding'
        ELSE partners.fname || ' ' || partners.lname 
        END AS pal, 
    CASE
        WHEN ticks.notes IS -1 THEN 'Nuthin'' to say' 
        ELSE ticks.notes
        END AS notes
    FROM
        ticks
        INNER JOIN climbs ON ticks.climb = climbs.id
        INNER JOIN areas ON climbs.area = areas.id
        INNER JOIN join_grades ON climbs.grade = join_grades.id
        INNER JOIN which_grades ON join_grades.id = which_grades.id
        INNER JOIN grades ON which_grades.grade = grades.id
        INNER JOIN join_types ON climbs.type = join_types.id
        INNER JOIN which_types ON join_types.id = which_types.id
        INNER JOIN climb_type ON which_types.type = climb_type.id
        INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
        INNER JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
        INNER JOIN partners ON climbed_with.partner_id = partners.id
    ORDER BY ticks.id DESC
    LIMIT 100000000
)
GROUP BY tick_id
ORDER BY date DESC;