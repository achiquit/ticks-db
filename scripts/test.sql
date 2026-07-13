SELECT
    -- sum(height)
    printf('%,d', SUM(ticks.height)) || 'ft' AS 'Feet Climbed'
FROM
    ticks;