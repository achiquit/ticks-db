SELECT
    date AS 'Date',
    SUM(height) AS 'Height'
FROM
    ticks
GROUP BY date
ORDER BY date desc;