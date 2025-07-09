.headers ON
.mode csv
.output /home/andre/Documents/websitejazzhands-1/resources/climb-locs.csv

SELECT 
    DISTINCT(SUBSTR(gps, 1, INSTR(gps, ', ') - 1)) AS 'Latitude',
    SUBSTRING(gps, INSTR(gps, ', ') + 1) AS 'Longitude',
    name
FROM
    climbs
WHERE gps != 'NULL';