SELECT
    areas.area_name AS 'Area',
    SUM(ticks.height) AS 'Height',
    COUNT(DISTINCT ticks.date) AS 'Days',
    areas.state || ', ' || areas.country AS 'Location'
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN areas ON areas.id = climbs.area
    INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    INNER JOIN climbed_with ON climbed_with.climbing_id = climbed_partners.id
    INNER JOIN partners ON partners.id = climbed_with.partner_id
GROUP BY areas.area_name, partners.id
HAVING ',' || group_concat(partners.id) || ',' LIKE '%,{partner},%'
ORDER BY SUM(ticks.height) ASC;