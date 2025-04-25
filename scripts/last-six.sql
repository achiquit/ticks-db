SELECT 
    ticks.date AS 'Date', climbs.name AS 'Climb Name', climbs.grade AS 'Grade', ticks.pitches AS 'Pitches', ticks.height AS 'Height', ticks.style AS 'Style', ticks.lead_style AS 'Lead Style', partners.fname || ' ' || partners.lname AS 'Partner / Belayer', ticks.notes AS 'Notes'
FROM 
    ticks 
    INNER JOIN climbs ON ticks.climb = climbs.id 
    INNER JOIN partners ON ticks.partner_id = partners.id
ORDER BY ticks.date DESC 
limit 6;