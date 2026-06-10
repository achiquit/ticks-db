SELECT
    partners.id AS 'Partner ID'
FROM
    climbed_partners
    INNER JOIN climbed_with ON climbed_with.climbing_id = climbed_partners.id
    INNER JOIN partners ON partners.id = climbed_with.partner_id
WHERE
    climbed_partners.id = 45
    OR climbed_partners.id = 84
    OR climbed_partners.id = 108;