SELECT partners.fname || ' ' || partners.lname AS 'Partner', COUNT(DISTINCT ticks.date) AS total_days, SUM(ticks.pitches) AS total_pitches, printf('%,d', SUM(height)) AS total_height, COUNT(DISTINCT climbs.area) AS total_areas
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
    JOIN partners ON climbed_with.partner_id = partners.id
WHERE NOT partners.id = -1
GROUP BY partners.id
ORDER BY total_days DESC
LIMIT 5;