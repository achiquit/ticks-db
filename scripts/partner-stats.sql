-- View all ticks with a given partner
SELECT 
    ticks.date AS 'Date', climbs.name AS 'Climb Name', climbs.grade AS 'Grade', ticks.pitches AS 'Pitches', ticks.height AS 'Height', ticks.style AS 'Style', ticks.success AS 'Lead Style', partners.fname || ' ' || partners.lname AS 'Partner / Belayer', ticks.notes AS 'Notes'
FROM 
    ticks 
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
    JOIN partners ON climbed_with.partner_id = partners.id
WHERE
    partners.id = 10
ORDER BY ticks.date DESC;


-- View aggregate days, height, and pitches with a given partner
SELECT 
    partners.fname || ' ' || partners.lname AS 'Partner / Belayer', COUNT(DISTINCT ticks.date) as 'Total Days', printf('%,d', SUM(ticks.height)) AS 'Total Height', SUM(ticks.pitches) AS 'Total Pitches', COUNT(DISTINCT climbs.area) AS 'Total Areas', COUNT(DISTINCT areas.country) AS 'Total Countries', COUNT(DISTINCT areas.state) AS 'Total States'
FROM 
    ticks
    INNER JOIN climbs ON ticks.climb = climbs.id
    INNER JOIN areas ON climbs.area = areas.id
    INNER JOIN climbed_partners ON ticks.climbed_id = climbed_partners.id
    JOIN climbed_with ON  climbed_partners.id = climbed_with.climbing_id
    JOIN partners ON climbed_with.partner_id = partners.id
WHERE
    partners.id = 10
ORDER BY ticks.date DESC;