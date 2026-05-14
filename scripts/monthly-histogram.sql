WITH RECURSIVE months(month_date) AS (
    SELECT date('now', 'start of month')
    UNION ALL
    SELECT date(month_date, '-1 month')
    FROM months
    WHERE date(month_date) >= date('now', '-59 months')
)
SELECT 
    strftime('%Y-%m', month_date) AS month,
    IFNULL(SUM(height), 0) height
FROM months
LEFT OUTER JOIN ticks ON strftime('%Y-%m', ticks.date) = month
GROUP BY month
ORDER BY month ASC;