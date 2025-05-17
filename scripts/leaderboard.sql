-- -- The old script that worked before I revamped the partners table setup
-- SELECT
--     (
--         SELECT COUNT(date)
--         FROM ticks
--         WHERE ticks.partner_id = partners.id AND NOT ticks.partner_id = -1
--     )
--     total_days,
--     (
--         SELECT SUM(pitches)
--         FROM ticks
--         WHERE ticks.partner_id = partners.id AND NOT ticks.partner_id = -1
--     )
--     total_pitches,
--     (
--         SELECT SUM(height)
--         FROM ticks
--         WHERE ticks.partner_id = partners.id AND NOT ticks.partner_id = -1
--     )
--     total_height,
--     (
--         SELECT COUNT(DISTINCT climbs.area)
--         FROM ticks
--             INNER JOIN climbs ON ticks.climb = climbs.id
--         WHERE ticks.partner_id = partners.id AND NOT ticks.partner_id = -1
--     )
--     total_areas,
--     partners.fname || ' ' || partners.lname AS 'Partner / Belayer'
-- FROM
--     partners
-- ORDER BY total_height DESC
-- LIMIT 5;

-- -- This code gets a list of all my ticks attributed to each partner I climbed with (like the most recent ticks but without the partners aggregated into a single, collective tick)
SELECT ticks.id, ticks.date, climbs.id, ticks.pitches, ticks.height, partners.id
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
    JOIN partners ON climbed_with.partner_id = partners.id
ORDER BY ticks.id DESC
LIMIT 30;


-- -- My WIP script
-- SELECT
--     (
--         SELECT COUNT(ticks.date)
--         FROM
--             ticks
--             INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
--             JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
--             JOIN partners ON climbed_with.partner_id = partners.id
--         WHERE climbed_with.partner_id = partners.id
--     )
--     total_height
-- FROM
--     partners
-- ORDER BY total_height DESC
-- LIMIT 5;