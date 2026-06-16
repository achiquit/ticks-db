SELECT 
    -- 'Guiding' AS 'Partner',
    COUNT(DISTINCT ticks.date) AS 'Days',
    SUM(ticks.pitches) AS 'Pitches',
    printf('%,d', SUM(ticks.height)) AS 'Height(ft)',
    COUNT(DISTINCT climbs.area) AS 'Areas'
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
WHERE ticks.guided_id > -1
;