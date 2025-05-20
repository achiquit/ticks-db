SELECT 
    strftime('%Y-%m', date) AS month,
    SUM(height) AS total_height,
    SUM(pitches) AS total_pitches,
    COUNT(id) AS climbs
FROM ticks
GROUP BY month
ORDER BY month DESC
LIMIT 6;