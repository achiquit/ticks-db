SELECT
    guided_id,
    GROUP_CONCAT(fname || ' ' || lname, ', ') AS clients
FROM
    guided_client
INNER JOIN
    clients ON clients.id = guided_client.client_id
GROUP BY
    guided_id;








-- SELECT
--     Title,
--     GROUP_CONCAT(name,';') track_list
-- FROM
--     tracks t
-- INNER JOIN albums a on a.AlbumId = t.AlbumId
-- GROUP BY
--     Title
-- ORDER BY
--     Title;