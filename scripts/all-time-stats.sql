SELECT
    COUNT(DISTINCT date) AS 'Days Climbed',
    printf('%,d', COUNT(DISTINCT ticks.id)) AS 'Ticks Made',
    printf('%,d', SUM(ticks.pitches)) AS 'Pitches Climbed',
    printf('%,d', SUM(height)) AS 'Feet Climbed',
    (COUNT(DISTINCT partner_id) -1) AS 'Partners',
    (COUNT(DISTINCT climb) -1) AS 'Climbs',
    (COUNT(DISTINCT area) -1) AS 'Areas',
    COUNT(DISTINCT country) AS 'Countries',
    COUNT(DISTINCT state) AS 'States'
FROM ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN areas ON climbs.area = areas.id
    INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    LEFT JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
    LEFT JOIN partners ON climbed_with.partner_id = partners.id;