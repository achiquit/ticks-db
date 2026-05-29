SELECT
    climbs.name,
    ticks.height,
    COUNT(ticks.height) AS 'count'
FROM ticks
INNER JOIN climbs ON ticks.climb = climbs.id
WHERE climbs.id = 527
GROUP BY ticks.height
ORDER BY 'count' DESC
LIMIT 5;

SELECT
    ticks.height
FROM ticks
INNER JOIN climbs ON ticks.climb = climbs.id
WHERE climbs.id = 527
GROUP BY ticks.height
ORDER BY COUNT(ticks.height) DESC
LIMIT 1;