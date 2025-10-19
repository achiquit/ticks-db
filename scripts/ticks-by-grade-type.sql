SELECT
    DISTINCT grades.grade,
    COUNT(ticks.id)
FROM
    grades
    INNER JOIN which_grades ON which_grades.grade = grades.id
    INNER JOIN join_grades ON join_grades.id = which_grades.id
    LEFT JOIN climbs ON climbs.grade = join_grades.id
    LEFT JOIN ticks ON ticks.climb = climbs.id
WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE '5.10' AND grades.grade NOT LIKE '5.11' AND grades.grade NOT LIKE '5.12' AND grades.grade NOT LIKE '5.13' AND grades.grade NOT LIKE '5.14' AND grades.grade NOT LIKE '5.15' AND climbs.type = 5
GROUP BY grades.grade
ORDER BY grades.id ASC;

-- SELECT
--     DISTINCT grades.grade,
--     CASE
--         WHEN climbs.type = 5 THEN
--             COUNT(ticks.id)
--         END AS 'Trad Count',
--     CASE
--         WHEN climbs.type = 4 THEN
--             COUNT(ticks.id)
--         END AS 'Sport Count'
-- FROM
--     grades
--     INNER JOIN which_grades ON which_grades.grade = grades.id
--     INNER JOIN join_grades ON join_grades.id = which_grades.id
--     LEFT JOIN climbs ON climbs.grade = join_grades.id
--     LEFT JOIN ticks ON ticks.climb = climbs.id
-- WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE '5.10' AND grades.grade NOT LIKE '5.11' AND grades.grade NOT LIKE '5.12' AND grades.grade NOT LIKE '5.13' AND grades.grade NOT LIKE '5.14' AND grades.grade NOT LIKE '5.15' AND climbs.type IN (4,5)
-- GROUP BY grades.grade
-- ORDER BY grades.id ASC;

-- Try switching around the joins to have it start with ticks again? 