SELECT
    COUNT(ticks.id) AS laps,
    climbs.name
FROM
    ticks
INNER JOIN
    climbs ON ticks.climb = climbs.id
GROUP BY climbs.id
ORDER BY laps DESC
LIMIT 10;