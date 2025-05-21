PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS climbed_with;
DROP TABLE IF EXISTS guided_client;
DROP TABLE IF EXISTS ticks;
DROP TABLE IF EXISTS climbed_partners;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS guided;
DROP TABLE IF EXISTS climbs;
DROP TABLE IF EXISTS areas;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS styles;
DROP TABLE IF EXISTS success;
DROP TABLE IF EXISTS commitment;
DROP TABLE IF EXISTS climb_type;
DROP TABLE IF EXISTS partners;

CREATE TABLE grades(
	"grade" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO grades (grade)
VALUES
	(-1),('5.1'),('5.2'),('5.3'),('5.4'),('5.5'),('5.6'),('5.7a'),('5.7'),('5.7d'),('5.8a'),('5.8'),('5.8d'),('5.9a'),('5.9'),('5.9d'),('5.10'),('5.10a'),('5.10b'),('5.10c'),('5.10d'),('5.11'),('5.11a'),('5.11b'),('5.11c'),('5.11d'),('5.12'),('5.12a'),('5.12b'),('5.12c'),('5.12d'),('5.13'),('5.13a'),('5.13b'),('5.13c'),('5.13d'),('A0'),('A1'),('A2'),('A3'),('A4'),('A5'),('C0'),('C1'),('C2'),('C3'),('C4'),('C5'),('Easy Snow'),('Moderate Snow'),('Difficult Snow'),('WI0'),('WI1'),('WI1a'),('WI1d'),('WI2'),('WI2a'),('WI2d'),('WI3'),('WI3a'),('WI3d'),('WI4'),('WI4a'),('WI4d'),('WI5'),('WI5a'),('WI5d'),('AI0'),('AI1'),('AI1a'),('AI1d'),('AI2'),('AI2a'),('AI2d'),('AI3'),('AI3a'),('AI3d'),('AI4'),('AI4a'),('AI4d'),('AI5'),('AI5a'),('AI5d'),('V0'),('V1'),('V1a'),('V1d'),('V2'),('V2a'),('V2d'),('V3a'),('V3d'),('V4'),('V4a'),('V4d'),('V5'),('V5a'),('V5d'),('V6'),('V6a'),('V6d'),('V7'),('V7a'),('V7d'),('V8'),('V8a'),('V8d'),('V9'),('V9a'),('V9d'),('V10'),('V10a'),('V10d'),('3rd'),('4th'),('5th'),('A'), ('B'), ('C'),('D'),('E'),('F');

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
	"type" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO climb_type (type)
VALUES
	(-1),('Boulder'),('TR'),('Sport'),('Trad'),('Alpine Ice'),('Water Ice'),('Aid'),('Via'), ('Snow'),('Scramble');

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
	"grade" TEXT NOT NULL,
	"commitment" TEXT,
	"type" TEXT NOT NULL,
	"gps" TEXT NOT NULL,
	"area" INTEGER NOT NULL,
	"notes" TEXT,
	FOREIGN KEY("area") REFERENCES areas("id"),
	FOREIGN KEY("type") REFERENCES climb_type("type")
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/climbs.csv climbs

CREATE TABLE clients(
	"id" INTEGER PRIMARY KEY ASC,
	"fname" TEXT NOT NULL,
    "lname" TEXT NOT NULL,
    "notes" TEXT
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/clients.csv clients

CREATE TABLE guided(
	"id" INTEGER PRIMARY KEY ASC,
	"company" TEXT NOT NULL,
	"tip" INTEGER,
	"notes" TEXT
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/guided.csv guided

CREATE TABLE climbed_partners(
	"id" INTEGER PRIMARY KEY ASC,
	"notes" TEXT
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/climbed_partners.csv climbed_partners

CREATE TABLE ticks(
	"id" INTEGER PRIMARY KEY ASC,
	"date" TEXT NOT NULL,
	"climb" INTEGER NOT NULL,
	"pitches" INTEGER NOT NULL,
	"height" INTEGER NOT NULL,
	"style" TEXT NOT NULL,
	"success" TEXT,
	"notes" TEXT,
	"climbed_id" INTEGER,
	"guided_id" INTEGER,
	FOREIGN KEY("climb") REFERENCES climbs("id"),
	FOREIGN KEY("style") REFERENCES styles('style'),
	FOREIGN KEY("success") REFERENCES success("style"),
	FOREIGN KEY("climbed_id") REFERENCES climbed_partners("id"),
	FOREIGN KEY("guided_id") REFERENCES guided("id")
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/ticks.csv ticks

CREATE TABLE guided_client(
	"guided_id" INTEGER NOT NULL,
	"client_id" INTEGER NOT NULL,
	PRIMARY KEY("guided_id", "client_id"),
	FOREIGN KEY("guided_id") REFERENCES guided("id"),
	FOREIGN KEY("client_id") REFERENCES clients("id")
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/guided_client.csv guided_client

CREATE TABLE climbed_with(
	"climbing_id" INTEGER NOT NULL,
	"partner_id" INTEGER NOT NULL,
	PRIMARY KEY("climbing_id", "partner_id"),
	FOREIGN KEY("climbing_id") REFERENCES climbed_partners("id"),
	FOREIGN KEY("partner_id") REFERENCES partners("id")
);
.mode csv
.import /home/andre/Documents/ticks-db/scripts/data/climbed_with.csv climbed_with

.header ON
.mode csv
.output /home/andre/Documents/websitejazzhands-1/climbing/data/last-six-ticks.csv
.read scripts/scripts/last-six.sql

.output /home/andre/Documents/websitejazzhands-1/climbing/data/all-ticks.csv
.read scripts/scripts/all-ticks.sql

.output /home/andre/Documents/websitejazzhands-1/climbing/data/all-time-stats.csv
.read scripts/scripts/all-time-stats.sql

.output /home/andre/Documents/websitejazzhands-1/climbing/data/partner-leaderboard.csv
.read scripts/scripts/leaderboard.sql