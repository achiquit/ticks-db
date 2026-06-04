SELECT
    COUNT(DISTINCT climbs.area)
FROM ticks
INNER JOIN climbs ON ticks.climb = climbs.id
INNER JOIN climbed_partners ON ticks.climbed_id = climbed_with.climbing_id
JOIN climbed_with ON climbed_partners.id = climbed_with.climbing_id
JOIN partners ON climbed_with.partner_id = partners.id
WHERE partners.id = 2;