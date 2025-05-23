SELECT tick_date AS 'Date', climb_name AS 'Climb', grade AS 'Grade', type AS 'Type', area AS 'Area', pitches AS 'Pitches', height as 'Height(ft)', style AS 'Style', success AS 'Success', group_concat(concat, ', ') AS 'Partner(s)', notes AS 'Notes'
FROM (
    SELECT ticks.id AS tick_id, ticks.date AS tick_date, climbs.name AS climb_name, climbs.grade AS grade, climbs.type AS type, areas.area_name AS area, ticks.pitches AS pitches, ticks.height AS height, ticks.style AS style, ticks.success AS success, 
    CASE 
        WHEN climbed_id IS -1 AND guided_id IS -1 THEN 'Unknown Partner'
        WHEN climbed_id IS -1 THEN 'Guiding'
        ELSE partners.fname || ' ' || partners.lname 
        END AS concat, 
    ticks.notes AS notes
    FROM
        ticks
        INNER JOIN climbs ON ticks.climb = climbs.id
        INNER JOIN areas ON climbs.area = areas.id
        INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
        LEFT JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
        LEFT JOIN partners ON climbed_with.partner_id = partners.id
    ORDER BY ticks.id DESC
    LIMIT 100000000
)
GROUP BY tick_id
ORDER BY date DESC;


    -- SELECT *
    -- FROM
    --     ticks
    --     INNER JOIN climbs ON ticks.climb = climbs.id
    --     INNER JOIN areas ON ticks.area = areas.id
    --     INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    --     LEFT JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
    --     LEFT JOIN partners ON climbed_with.partner_id = partners.id
    -- ORDER BY ticks.id DESC
    -- LIMIT 10;