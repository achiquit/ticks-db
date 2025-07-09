SELECT 
    strftime('%Y', date) AS year,
    SUM(height) AS height
FROM ticks
GROUP BY year
ORDER BY year ASC;