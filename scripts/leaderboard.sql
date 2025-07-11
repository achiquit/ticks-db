SELECT partners.fname || ' ' || partners.lname AS 'Partner', COUNT(DISTINCT ticks.date) AS 'Days', SUM(ticks.pitches) AS 'Pitches', printf('%,d', SUM(height)) AS 'Height(ft)', COUNT(DISTINCT climbs.area) AS 'Areas'
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
    JOIN partners ON climbed_with.partner_id = partners.id
WHERE NOT partners.id = -1
GROUP BY partners.id
UNION
SELECT 'Guiding' AS 'Partner', COUNT(DISTINCT ticks.date) AS 'Days', SUM(ticks.pitches) AS 'Pitches', printf('%,d', SUM(height)) AS 'Height(ft)', COUNT(DISTINCT climbs.area) AS 'Areas'
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
    JOIN partners ON climbed_with.partner_id = partners.id
WHERE partners.id = -1 AND guided_id != -1;