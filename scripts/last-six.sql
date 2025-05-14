SELECT ticks.id AS 'Tick ID', ticks.date AS 'Date', climbs.name AS 'Climb Name', climbs.grade AS 'Grade', ticks.pitches AS 'Pitches', ticks.height AS 'Height', ticks.style AS 'Style', ticks.success AS 'Success', partners.fname || ' ' || partners.lname AS 'Partner / Belayer', ticks.notes AS 'Notes'
FROM
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    LEFT JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
    LEFT JOIN partners ON climbed_with.partner_id = partners.id
ORDER BY ticks.id DESC
LIMIT 30;