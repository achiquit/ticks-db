-- SELECT
--     grades.grade,
--     count(ticks.id)
-- FROM
--     grades
--     INNER JOIN climbs ON grades.id = climbs.grade
--     INNER JOIN ticks ON climbs.id = ticks.climb
-- WHERE grades.id = 2;

WITH 
    countUp AS (SELECT 2 as n
                UNION all
                SELECT n+1 FROM countUp WHERE n < 30)
SELECT
    n,
    grades.grade,
    count(ticks.id)
FROM countUp
    INNER JOIN grades ON grades.id = countUp.n
    INNER JOIN climbs ON climbs.grade = grades.id
    INNER JOIN ticks ON climbs.id = ticks.climb
WHERE grades.id = n;