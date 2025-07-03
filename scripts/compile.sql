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
.import /home/andre/Documents/ticks-db/scripts/data/grades.csv grades

CREATE TABLE join_grades(
	"id" INTEGER PRIMARY KEY ASC,
	"notes" TEXT
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/join_grades.csv join_grades

CREATE TABLE which_grades(
	"id" INTEGER ASC NOT NULL,
	"grade" INTEGER NOT NULL,
	PRIMARY KEY ("id", "grade"),
	FOREIGN KEY("id") REFERENCES join_grades("id"),
	FOREIGN KEY("grade") REFERENCES grades("id")
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/which_grades.csv which_grades

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

CREATE TABLE commitment(
	"type" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO commitment (type)
VALUES
	(-1),('G'),('PG'),('PG13'),('R'),('X');

CREATE TABLE climb_type(
	"id" INTEGER PRIMARY KEY ASC,
	"type" TEXT NOT NULL
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/types.csv climb_type

CREATE TABLE join_types(
	"id" INTEGER PRIMARY KEY ASC,
	"notes" TEXT
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/join_types.csv join_types

CREATE TABLE which_types(
	"id" INTEGER ASC NOT NULL,
	"type" TEXT NOT NULL,
	PRIMARY KEY ("id", "type"),
	FOREIGN KEY("type") REFERENCES climb_type("id"),
	FOREIGN KEY("id") REFERENCES join_types("id")
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/which_types.csv which_types

CREATE TABLE partners(
	"id" INTEGER PRIMARY KEY ASC,
	"fname" TEXT NOT NULL,
	"lname" TEXT NOT NULL,
	"notes" TEXT
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/partners.csv partners

CREATE TABLE areas(
	"id" INTEGER PRIMARY KEY ASC,
	"area_name" TEXT NOT NULL,
	"country" TEXT NOT NULL,
	"state" TEXT NOT NULL,
	"notes" TEXT
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/areas.csv areas

CREATE TABLE climbs(
	"id" INTEGER PRIMARY KEY ASC,
	"name" TEXT NOT NULL,
	"grade" INTEGER NOT NULL,
	"commitment" TEXT,
	"type" INTEGER NOT NULL,
	"gps" TEXT NOT NULL,
	"area" INTEGER NOT NULL,
	"notes" TEXT,
	FOREIGN KEY("grade") REFERENCES join_grades("id"),
	FOREIGN KEY("type") REFERENCES join_types("id"),
	FOREIGN KEY("area") REFERENCES areas("id")
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/climbs.csv climbs

-- CREATE TABLE clients(
-- 	"id" INTEGER PRIMARY KEY ASC,
-- 	"fname" TEXT NOT NULL,
--     "lname" TEXT NOT NULL,
--     "notes" TEXT
-- );
-- .mode csv
-- .import /home/andre/Documents/ticks-db/scripts/data/clients.csv clients

-- CREATE TABLE guided(
-- 	"id" INTEGER PRIMARY KEY ASC,
-- 	"company" TEXT NOT NULL,
-- 	"tip" INTEGER,
-- 	"notes" TEXT
-- );
-- .mode csv
-- .import /home/andre/Documents/ticks-db/scripts/data/guided.csv guided

-- CREATE TABLE climbed_partners(
-- 	"id" INTEGER PRIMARY KEY ASC,
-- 	"notes" TEXT
-- );
-- .mode csv
-- .import /home/andre/Documents/ticks-db/scripts/data/climbed_partners.csv climbed_partners

-- CREATE TABLE ticks(
-- 	"id" INTEGER PRIMARY KEY ASC,
-- 	"date" TEXT NOT NULL,
-- 	"climb" INTEGER NOT NULL,
-- 	"pitches" INTEGER NOT NULL,
-- 	"height" INTEGER NOT NULL,
-- 	"style" INTEGER NOT NULL,
-- 	"success" TEXT,
-- 	"notes" TEXT,
-- 	"climbed_id" INTEGER,
-- 	"guided_id" INTEGER,
-- 	FOREIGN KEY("climb") REFERENCES climbs("id"),
-- 	FOREIGN KEY("style") REFERENCES styles("style"),
-- 	FOREIGN KEY("success") REFERENCES success("style"),
-- 	FOREIGN KEY("climbed_id") REFERENCES climbed_partners("id"),
-- 	FOREIGN KEY("guided_id") REFERENCES guided("id")
-- );
-- .mode csv
-- .import /home/andre/Documents/ticks-db/scripts/data/ticks.csv ticks

-- CREATE TABLE guided_client(
-- 	"guided_id" INTEGER NOT NULL,
-- 	"client_id" INTEGER NOT NULL,
-- 	PRIMARY KEY("guided_id", "client_id"),
-- 	FOREIGN KEY("guided_id") REFERENCES guided("id"),
-- 	FOREIGN KEY("client_id") REFERENCES clients("id")
-- );
-- .mode csv
-- .import /home/andre/Documents/ticks-db/scripts/data/guided_client.csv guided_client

-- CREATE TABLE climbed_with(
-- 	"climbing_id" INTEGER NOT NULL,
-- 	"partner_id" INTEGER NOT NULL,
-- 	PRIMARY KEY("climbing_id", "partner_id"),
-- 	FOREIGN KEY("climbing_id") REFERENCES climbed_partners("id"),
-- 	FOREIGN KEY("partner_id") REFERENCES partners("id")
-- );
-- .mode csv
-- .import /home/andre/Documents/ticks-db/scripts/data/climbed_with.csv climbed_with

-- .output /home/andre/Documents/websitejazzhands-1/climbing/data/all-ticks.csv
-- .read scripts/scripts/all-ticks.sql

-- .output /home/andre/Documents/websitejazzhands-1/climbing/data/all-time-stats.csv
-- .read scripts/scripts/all-time-stats.sql

-- .output /home/andre/Documents/websitejazzhands-1/climbing/data/partner-leaderboard.csv
-- .read scripts/scripts/leaderboard.sql

-- .mode table