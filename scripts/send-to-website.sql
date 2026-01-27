.headers ON
.mode csv
.output ../websitejazzhands/climbing/data/all-ticks.csv
.read scripts/all-ticks.sql

.output ../websitejazzhands/climbing/data/all-time-stats.csv
.read scripts/stats-over-time.sql

.output ../websitejazzhands/climbing/data/partner-leaderboard.csv
.read scripts/leaderboard.sql

.output ../websitejazzhands/climbing/data/climb-locs.csv
.read scripts/climbs-map.sql

.output ../websitejazzhands/climbing/data/monthly-height.csv
.read scripts/monthly-histogram.sql

.output ../websitejazzhands/climbing/data/yearly-height.csv
.read scripts/yearly-height.sql

.output ../websitejazzhands/climbing/data/top-climbs.csv
.read scripts/top-climbs.sql

.output ../websitejazzhands/climbing/data/ticks-by-grade.csv
.read scripts/ticks-by-grade.sql