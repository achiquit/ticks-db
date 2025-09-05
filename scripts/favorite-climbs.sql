SELECT
    climbs.name,
    COUNT(ticks.id) AS guide_laps
FROM
    ticks
    INNER JOIN climbs ON climbs.id = ticks.climb
GROUP BY climbs.id
UNION ALL
SELECT
    climbs.name,
    COUNT(ticks.id) AS total_laps
FROM
    ticks
    INNER JOIN climbs ON climbs.id = ticks.climb
GROUP BY climbs.id
ORDER BY total_laps DESC;