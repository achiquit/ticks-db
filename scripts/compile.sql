PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS climbed_with;
DROP TABLE IF EXISTS guided_client;
DROP TABLE IF EXISTS ticks;
DROP TABLE IF EXISTS climbed_partners;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS guided;
DROP TABLE IF EXISTS climbs;
DROP TABLE IF EXISTS areas;
DROP TABLE IF EXISTS which_grades;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS styles;
DROP TABLE IF EXISTS success;
DROP TABLE IF EXISTS danger;
DROP TABLE IF EXISTS commitment;
DROP TABLE IF EXISTS which_types;
DROP TABLE IF EXISTS climb_type;
DROP TABLE IF EXISTS partners;
DROP TABLE IF EXISTS join_types;
DROP TABLE IF EXISTS join_grades;

CREATE TABLE grades(
	"id" INTEGER PRIMARY KEY ASC,
	"grade" TEXT NOT NULL
);
.mode csv
.import data/grades.csv grades

CREATE TABLE join_grades(
	"id" INTEGER PRIMARY KEY ASC,
	"notes" TEXT
);
.mode csv
.import data/join_grades.csv join_grades

CREATE TABLE which_grades(
	"id" INTEGER ASC NOT NULL,
	"grade" INTEGER NOT NULL,
	PRIMARY KEY ("id", "grade"),
	FOREIGN KEY("id") REFERENCES join_grades("id"),
	FOREIGN KEY("grade") REFERENCES grades("id")
);
.mode csv
.import data/which_grades.csv which_grades

CREATE TABLE styles(
	"style" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO styles (style)
VALUES
	(-1),('Lead'),('TR'),('LRS'),('TRS'),('Solo'),('Follow'),('Send'),('Attempt'),('Flash');

CREATE TABLE success(
	"style" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO success (style)
VALUES
	('-1'),('Fell/Hung'),('Pinkpoint'),('Redpoint'),('Onsight'),('Flash'),('Clean'), ('Attempt');

CREATE TABLE danger(
	"type" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO danger (type)
VALUES
	(-1),('G'),('PG'),('PG13'),('R'),('X');

CREATE TABLE commitment(
	"level" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO commitment (level)
VALUES
	('-1'), ('I'), ('II'), ('III'), ('IV'), ('V'), ('VI'), ('VII');

CREATE TABLE climb_type(
	"id" INTEGER PRIMARY KEY ASC,
	"type" TEXT NOT NULL
);
.mode csv
.import data/types.csv climb_type

CREATE TABLE join_types(
	"id" INTEGER PRIMARY KEY ASC,
	"notes" TEXT
);
.mode csv
.import data/join_types.csv join_types

CREATE TABLE which_types(
	"id" INTEGER ASC NOT NULL,
	"type" INTEGER NOT NULL,
	PRIMARY KEY ("id", "type"),
	FOREIGN KEY("type") REFERENCES climb_type("id"),
	FOREIGN KEY("id") REFERENCES join_types("id")
);
.mode csv
.import data/which_types.csv which_types

CREATE TABLE partners(
	"id" INTEGER PRIMARY KEY ASC,
	"fname" TEXT NOT NULL,
	"lname" TEXT NOT NULL,
	"notes" TEXT
);
.mode csv
.import data/partners.csv partners

CREATE TABLE areas(
	"id" INTEGER PRIMARY KEY ASC,
	"area_name" TEXT NOT NULL,
	"country" TEXT NOT NULL,
	"state" TEXT NOT NULL,
	"notes" TEXT
);
.mode csv
.import data/areas.csv areas

CREATE TABLE climbs(
	"id" INTEGER PRIMARY KEY ASC,
	"name" TEXT NOT NULL,
	"grade" INTEGER NOT NULL,
	"danger" TEXT,
	"type" INTEGER NOT NULL,
	"commitment" TEXT NOT NULL,
	"gps" TEXT NOT NULL,
	"area" INTEGER NOT NULL,
	"notes" TEXT,
	FOREIGN KEY("grade") REFERENCES join_grades("id"),
	FOREIGN KEY("type") REFERENCES join_types("id"),
	FOREIGN KEY("commitment") REFERENCES commitment("level"),
	FOREIGN KEY("area") REFERENCES areas("id")
);
.mode csv
.import data/climbs.csv climbs

CREATE TABLE clients(
	"id" INTEGER PRIMARY KEY ASC,
	"fname" TEXT NOT NULL,
    "lname" TEXT NOT NULL,
    "notes" TEXT
);
.mode csv
.import data/clients.csv clients

CREATE TABLE guided(
	"id" INTEGER PRIMARY KEY ASC,
	"company" TEXT NOT NULL,
	"tip" INTEGER,
	"notes" TEXT
);
.mode csv
.import data/guided.csv guided

CREATE TABLE climbed_partners(
	"id" INTEGER PRIMARY KEY ASC,
	"notes" TEXT
);
.mode csv
.import data/climbed_partners.csv climbed_partners

CREATE TABLE ticks(
	"id" INTEGER PRIMARY KEY ASC,
	"date" TEXT NOT NULL,
	"climb" INTEGER NOT NULL,
	"pitches" INTEGER NOT NULL,
	"height" INTEGER NOT NULL,
	"style" INTEGER NOT NULL,
	"success" TEXT,
	"notes" TEXT,
	"climbed_id" INTEGER,
	"guided_id" INTEGER,
	FOREIGN KEY("climb") REFERENCES climbs("id"),
	FOREIGN KEY("style") REFERENCES styles("style"),
	FOREIGN KEY("success") REFERENCES success("style"),
	FOREIGN KEY("climbed_id") REFERENCES climbed_partners("id"),
	FOREIGN KEY("guided_id") REFERENCES guided("id")
);
.mode csv
.import data/ticks.csv ticks

CREATE TABLE guided_client(
	"guided_id" INTEGER NOT NULL,
	"client_id" INTEGER NOT NULL,
	PRIMARY KEY("guided_id", "client_id"),
	FOREIGN KEY("guided_id") REFERENCES guided("id"),
	FOREIGN KEY("client_id") REFERENCES clients("id")
);
.mode csv
.import data/guided_client.csv guided_client

CREATE TABLE climbed_with(
	"climbing_id" INTEGER NOT NULL,
	"partner_id" INTEGER NOT NULL,
	PRIMARY KEY("climbing_id", "partner_id"),
	FOREIGN KEY("climbing_id") REFERENCES climbed_partners("id"),
	FOREIGN KEY("partner_id") REFERENCES partners("id")
);
.mode csv
.import data/climbed_with.csv climbed_with

.headers ON
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

.mode table