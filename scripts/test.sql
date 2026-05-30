DROP TABLE IF EXISTS climbs_test;
CREATE TABLE climbs_test AS
SELECT * FROM climbs; 

select * from climbs_test order by id desc limit 5;

-- SELECT
--     climbs.name,
--     ticks.height,
--     COUNT(ticks.height) AS 'count'
-- FROM ticks
-- INNER JOIN climbs ON ticks.climb = climbs.id
-- WHERE climbs.id = 527
-- GROUP BY ticks.height
-- ORDER BY 'count' DESC
-- LIMIT 5;