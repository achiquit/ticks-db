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

SELECT
    (
        SELECT COUNT(DISTINCT(date))
        FROM ticks
        INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
        LEFT JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
        LEFT JOIN partners ON climbed_with.partner_id = partners.id
        WHERE
    )
FROM
