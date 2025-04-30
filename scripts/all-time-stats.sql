SELECT
    COUNT(DISTINCT date) AS 'Days Climbed',
    printf('%,d', SUM(ticks.pitches)) AS 'Pitches Climbed',
    printf('%,d', SUM(height)) AS 'Feet Climbed',
    COUNT(DISTINCT partner_id) AS 'Partners',
    COUNT(DISTINCT climb) AS 'Climbs',
    COUNT(DISTINCT area) AS 'Areas',
    COUNT(DISTINCT country) AS 'Countries',
    COUNT(DISTINCT state) AS 'States'
FROM ticks
    INNER JOIN partners ON ticks.partner_id = partners.id
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN areas ON climbs.area = areas.id;