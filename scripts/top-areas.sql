SELECT
    areas.area_name AS 'Area',
    COUNT(DISTINCT ticks.date) AS 'Days',
    printf("%,d", SUM(ticks.height)) || 'ft' AS 'Height',
    areas.state || ', ' || areas.country AS 'Location'
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN areas ON areas.id = climbs.area
GROUP BY areas.area_name
ORDER BY SUM(ticks.height) ASC;