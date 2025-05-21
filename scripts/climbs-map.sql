.headers OFF
.mode csv
.output /home/andre/Documents/climb-locs.csv

SELECT 
    DISTINCT(SUBSTR(gps, 1, INSTR(gps, ', ') - 1)) AS 'Latitude',
    SUBSTRING(gps, INSTR(gps, ', ') + 1) AS 'Longitude',
    name
FROM
    climbs
WHERE gps != 'NULL';