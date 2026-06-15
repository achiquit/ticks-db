-- Fell/Hung on TR
SELECT
    grades.id AS 'ID',
    grades.grade AS 'Grade',
    COUNT(ticks.id) AS 'Count',
    'Fell/Hung' AS 'Success',
    'TR/Follow' AS 'Style'
FROM
    grades
    INNER JOIN which_grades ON which_grades.grade = grades.id
    INNER JOIN join_grades ON join_grades.id = which_grades.id
    LEFT JOIN climbs ON climbs.grade = join_grades.id
    LEFT JOIN ticks ON ticks.climb = climbs.id
WHERE ticks.success LIKE 'Fell/Hung' AND ticks.style LIKE 'TR' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Fell/Hung' AND ticks.style LIKE 'Follow' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Fell/Hung' AND ticks.style LIKE 'TRS' AND grades.grade LIKE '5.%'
GROUP BY grades.grade

UNION

-- Fell/Hung on lead
SELECT
    grades.id AS 'ID',
    grades.grade AS 'Grade',
    COUNT(ticks.id) AS 'Count',
    'Fell/Hung' AS 'Success',
    'Lead' AS 'Style'
FROM
    grades
    INNER JOIN which_grades ON which_grades.grade = grades.id
    INNER JOIN join_grades ON join_grades.id = which_grades.id
    LEFT JOIN climbs ON climbs.grade = join_grades.id
    LEFT JOIN ticks ON ticks.climb = climbs.id
WHERE ticks.success LIKE 'Fell/Hung' AND ticks.style LIKE 'Lead' AND grades.grade LIKE '5.%'
GROUP BY grades.grade

UNION

-- Fell/Hung on LRS
SELECT
    grades.id AS 'ID',
    grades.grade AS 'Grade',
    COUNT(ticks.id) AS 'Count',
    'Fell/Hung' AS 'Success',
    'LRS' AS 'Style'
FROM
    grades
    INNER JOIN which_grades ON which_grades.grade = grades.id
    INNER JOIN join_grades ON join_grades.id = which_grades.id
    LEFT JOIN climbs ON climbs.grade = join_grades.id
    LEFT JOIN ticks ON ticks.climb = climbs.id
WHERE ticks.success LIKE 'Fell/Hung' AND ticks.style LIKE 'LRS' AND grades.grade LIKE '5.%'
GROUP BY grades.grade

UNION

-- Sent on TR
SELECT
    grades.id AS 'ID',
    grades.grade AS 'Grade',
    COUNT(ticks.id) AS 'Count',
    'Send' AS 'Success',
    'TR/Follow' AS 'Style'
FROM
    grades
    INNER JOIN which_grades ON which_grades.grade = grades.id
    INNER JOIN join_grades ON join_grades.id = which_grades.id
    LEFT JOIN climbs ON climbs.grade = join_grades.id
    LEFT JOIN ticks ON ticks.climb = climbs.id
WHERE ticks.success LIKE 'Clean' AND ticks.style LIKE 'TR' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Clean' AND ticks.style LIKE 'Follow' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Clean' AND ticks.style LIKE 'TRS' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Flash' AND ticks.style LIKE 'TR' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Flash' AND ticks.style LIKE 'Follow' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Flash' AND ticks.style LIKE 'TRS' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Onsight' AND ticks.style LIKE 'TR' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Onsight' AND ticks.style LIKE 'Follow' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Onsight' AND ticks.style LIKE 'TRS' AND grades.grade LIKE '5.%'
GROUP BY grades.grade

UNION

-- Sent on lead
SELECT
    grades.id AS 'ID',
    grades.grade AS 'Grade',
    COUNT(ticks.id) AS 'Count',
    'Send' AS 'Success',
    'Lead' AS 'Style'
FROM
    grades
    INNER JOIN which_grades ON which_grades.grade = grades.id
    INNER JOIN join_grades ON join_grades.id = which_grades.id
    LEFT JOIN climbs ON climbs.grade = join_grades.id
    LEFT JOIN ticks ON ticks.climb = climbs.id
WHERE ticks.success LIKE 'Redpoint' AND ticks.style LIKE 'Lead' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Pinkpoint' AND ticks.style LIKE 'Lead' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Onsight' AND ticks.style LIKE 'Lead' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Flash' AND ticks.style LIKE 'Lead' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Clean' AND ticks.style LIKE 'Lead' AND grades.grade LIKE '5.%'
GROUP BY grades.grade

UNION

-- Sent on LRS
SELECT
    grades.id AS 'ID',
    grades.grade AS 'Grade',
    COUNT(ticks.id) AS 'Count',
    'Send' AS 'Success',
    'LRS' AS 'Style'
FROM
    grades
    INNER JOIN which_grades ON which_grades.grade = grades.id
    INNER JOIN join_grades ON join_grades.id = which_grades.id
    LEFT JOIN climbs ON climbs.grade = join_grades.id
    LEFT JOIN ticks ON ticks.climb = climbs.id
WHERE ticks.success LIKE 'Redpoint' AND ticks.style LIKE 'LRS' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Pinkpoint' AND ticks.style LIKE 'LRS' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Onsight' AND ticks.style LIKE 'LRS' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Flash' AND ticks.style LIKE 'LRS' AND grades.grade LIKE '5.%'
    OR ticks.success LIKE 'Clean' AND ticks.style LIKE 'LRS' AND grades.grade LIKE '5.%'
GROUP BY grades.grade;