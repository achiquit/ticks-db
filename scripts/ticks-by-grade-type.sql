SELECT
    grades.grade AS grade,
    climb_type.type AS climb_type,
    COUNT(ticks.id) AS 'da count'
FROM
    grades
    FULL JOIN which_grades ON which_grades.grade = grades.id
    FULL JOIN join_grades ON join_grades.id = which_grades.id
    FULL JOIN climbs ON climbs.grade = join_grades.id
    FULL JOIN ticks ON ticks.climb = climbs.id
    FULL JOIN join_types ON join_types.id = climbs.type
    FULL JOIN which_types ON which_types.id = join_types.id
    FULL JOIN climb_type ON climb_type.id = which_types.type
WHERE
    (grades.grade LIKE '5.%' AND grades.grade NOT LIKE '5.15d') AND (climbs.type IN (4,5))
GROUP BY climb_type.type, grades.grade
ORDER BY grades.id ASC;

-- The above code works! The resulting table is just in the wrong shape for me to build a graph out of it. Another issue that must be dealt with is that I don't get 0 values when I filter grades AND climb types, they're skipped.

-- DROP TABLE IF EXISTS dummy;

-- CREATE TABLE dummy(
--     "id" INTEGER ASC NOT NULL,
--     "type" TEXT NOT NULL,
--     "grade" TEXT NOT NULL
-- );
-- .mode csv
-- .import training/dummy-data.csv dummy

-- .mode column

-- SELECT
--     DISTINCT grade,
--     type,
--     SUM()
-- FROM
--     dummy
-- GROUP BY
--     grade,
--     type
-- ORDER BY 
--     grade ASC,
--     type ASC;