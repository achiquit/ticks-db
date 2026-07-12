SELECT
    areas.id AS 'ID',
    areas.area_name AS 'Area',
    COUNT(DISTINCT ticks.date) AS 'Days',
    SUM(ticks.height) AS 'Height',
    areas.state || ', ' || areas.country AS 'Location'
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN areas ON areas.id = climbs.area
WHERE ticks.guided_id > -1
GROUP BY climbs.area
ORDER BY COUNT(DISTINCT ticks.date) DESC, SUM(ticks.height) DESC;