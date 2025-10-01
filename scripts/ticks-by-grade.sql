-- SELECT
--     DISTINCT grades.grade,
--     COUNT(*) AS count
-- FROM
--     grades
--     INNER JOIN which_grades ON which_grades.grade = grades.id
--     INNER JOIN join_grades ON join_grades.id = which_grades.id
--     LEFT JOIN climbs ON climbs.grade = join_grades.id
--     LEFT JOIN ticks ON ticks.climb = climbs.id
-- WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE '5.10' AND grades.grade NOT LIKE '5.11' AND grades.grade NOT LIKE '5.12' AND grades.grade NOT LIKE '5.13' AND grades.grade NOT LIKE '5.14' AND grades.grade NOT LIKE '5.15'
-- GROUP BY grades.grade
-- ORDER BY grades.id DESC;

SELECT
    DISTINCT grades.grade,
    COUNT(*) AS count
FROM
    grades
    INNER JOIN which_grades ON which_grades.grade = grades.id
    INNER JOIN join_grades ON join_grades.id = which_grades.id
    INNER JOIN climbs ON climbs.grade = join_grades.id
    INNER JOIN ticks ON ticks.climb = climbs.id
WHERE grades.grade LIKE '5.%' AND grades.grade NOT LIKE '5.10' AND grades.grade NOT LIKE '5.11' AND grades.grade NOT LIKE '5.12' AND grades.grade NOT LIKE '5.13' AND grades.grade NOT LIKE '5.14' AND grades.grade NOT LIKE '5.15'
GROUP BY grades.grade
ORDER BY grades.id DESC;