SELECT
    (
        SELECT COUNT(date)
        FROM ticks
        WHERE ticks.partner_id = partners.id
    )
    total_days,
    (
        SELECT SUM(pitches)
        FROM ticks
        WHERE ticks.partner_id = partners.id
    )
    total_pitches,
    (
        SELECT SUM(height)
        FROM ticks
        WHERE ticks.partner_id = partners.id
    )
    total_height,
    (
        SELECT COUNT(DISTINCT area)
        FROM ticks
        WHERE ticks.partner_id = partners.id
    )
    total_areas,
    partners.fname || ' ' || partners.lname AS 'Partner / Belayer'
FROM
    partners
ORDER BY total_days DESC
LIMIT 5;