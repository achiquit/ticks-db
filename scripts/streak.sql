WITH ClimbingStreak AS (
    SELECT
        date,
        JULIANDAY(date) AS grp
    FROM
        ticks
),
ConsecutiveCounts AS (
    SELECT
        grp,
        COUNT(*) AS consecutive_days
    FROM
        ClimbingStreak
    GROUP BY
        grp
)
SELECT
    MAX(consecutive_days) AS max_consecutive_dates
FROM
    ConsecutiveCounts;