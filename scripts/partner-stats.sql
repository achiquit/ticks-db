-- View all ticks with a given partner
SELECT 
    ticks.date AS 'Date', climbs.name AS 'Climb Name', climbs.grade AS 'Grade', ticks.pitches AS 'Pitches', ticks.height AS 'Height', ticks.style AS 'Style', ticks.success AS 'Lead Style', partners.fname || ' ' || partners.lname AS 'Partner / Belayer', ticks.notes AS 'Notes'
FROM 
    ticks 
    INNER JOIN climbs ON ticks.climb = climbs.id 
    INNER JOIN partners ON ticks.partner_id = partners.id
WHERE
    partners.id = 10
ORDER BY ticks.date DESC;


-- View aggregate days, height, and pitches with a given partner
SELECT 
    COUNT(DISTINCT ticks.date) as 'Total Days', SUM(ticks.height) AS 'Total Height', SUM(ticks.pitches) AS 'Total Pitches', partners.fname || ' ' || partners.lname AS 'Partner / Belayer'
FROM 
    ticks
    INNER JOIN partners ON ticks.partner_id = partners.id
WHERE
    partners.id = 10
ORDER BY ticks.date DESC;