-- SELECT
--     MAX(consecutive_count) AS longest_consecutive_streak,
--     grp
-- FROM
--     (SELECT
--         grp,
--         COUNT(*) AS consecutive_count
--     FROM
--         (SELECT
--             date,
--             JULIANDAY(date) - ROW_NUMBER() OVER (ORDER BY date) AS grp
--         FROM
--             ticks) AS grouped_events
--     GROUP BY
--         grp);

SELECT
    date,
    grp,
    COUNT(*) AS consecutive_count
FROM
    (SELECT
        date,
        JULIANDAY(date) - ROW_NUMBER() OVER (ORDER BY date) AS grp
    FROM
        ticks) AS grouped_events
GROUP BY
    grp
ORDER BY consecutive_count ASC