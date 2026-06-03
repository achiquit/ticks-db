SELECT
    date AS 'Date',
    climbs.name AS 'Climb',
    areas.area_name AS 'Area',
    ticks.height AS 'Height',
    climbs.gps AS 'Loc'
FROM TICKS
INNER JOIN climbs ON climbs.id = ticks.climb
INNER JOIN areas ON climbs.area = areas.id
ORDER BY date DESC
LIMIT 5;