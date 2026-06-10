-- Direct To Website Scripts
.headers ON
.mode csv
.output ../websitejazzhands/climbing/data/all-ticks.csv
.read scripts/all-ticks.sql

.output ../websitejazzhands/climbing/data/all-time-stats.csv
.read scripts/stats-over-time.sql

.output ../websitejazzhands/climbing/data/partner-leaderboard.csv
.read scripts/leaderboard.sql

.output ../websitejazzhands/climbing/data/top-climbs.csv
.read scripts/top-climbs.sql

.output ../websitejazzhands/climbing/data/top-areas.csv
.read scripts/top-areas.sql

-- To Data Folder Scripts
.output data/yearly-height.csv
.read scripts/yearly-height.sql

.output data/monthly-height.csv
.read scripts/monthly-height.sql

.output data/overview-stats.csv
.read scripts/stats-over-time.sql

.output data/climb-locs.csv
.read scripts/climbs-map.sql

.output data/climb-locs-heat.csv
.read scripts/climbs-heatmap.sql

.output data/grades_by_date.csv
.read scripts/grades_by_date.sql