PRAGMA foreign_keys = OFF;
DROP TABLE IF EXISTS guided;
DROP TABLE IF EXISTS ticks;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS climbs;
DROP TABLE IF EXISTS areas;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS styles;
DROP TABLE IF EXISTS lead_styles;
DROP TABLE IF EXISTS commitment;
DROP TABLE IF EXISTS climb_type;

CREATE TABLE grades(
	"grade" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO grades (grade)
VALUES
	('5.1'),('5.2'),('5.3'),('5.4'),('5.5'),('5.6'),('5.7a'),('5.7'),('5.7d'),('5.8a'),('5.8'),('5.8d'),('5.9a'),('5.9'),('5.9d'),('5.10'),('5.10a'),('5.10b'),('5.10c'),('5.10d'),('5.11'),('5.11a'),('5.11b'),('5.11c'),('5.11d'),('5.12'),('5.12a'),('5.12b'),('5.12c'),('5.12d'),('5.13'),('5.13a'),('5.13b'),('5.13c'),('5.13d'),('A0'),('A1'),('A2'),('A3'),('A4'),('A5'),('C0'),('C1'),('C2'),('C3'),('C4'),('C5'),('Easy Snow'),('Moderate Snow'),('Difficult Snow'),('WI0'),('WI1'),('WI1a'),('WI1d'),('WI2'),('WI2a'),('WI2d'),('WI3'),('WI3a'),('WI3d'),('WI4'),('WI4a'),('WI4d'),('WI5'),('WI5a'),('WI5d'),('AI0'),('AI1'),('AI1a'),('AI1d'),('AI2'),('AI2a'),('AI2d'),('AI3'),('AI3a'),('AI3d'),('AI4'),('AI4a'),('AI4d'),('AI5'),('AI5a'),('AI5d'),('V0'),('V1'),('V1a'),('V1d'),('V2'),('V2a'),('V2d'),('V3a'),('V3d'),('V4'),('V4a'),('V4d'),('V5'),('V5a'),('V5d'),('V6'),('V6a'),('V6d'),('V7'),('V7a'),('V7d'),('V8'),('V8a'),('V8d'),('V9'),('V9a'),('V9d'),('V10'),('V10a'),('V10d'),('3rd'),('4th'),('5th');

CREATE TABLE styles(
	"style" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO styles (style)
VALUES
	('lead'),('TR'),('LRS'),('TRS'),('solo'),('follow');

CREATE TABLE lead_styles(
	"style" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO lead_styles (style)
VALUES
	('fell/hung'),('pinkpoint'),('redpoint'),('onsight'),('flash'),('clean');

CREATE TABLE commitment(
	"type" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO commitment (type)
VALUES
	('G'),('PG'),('PG-13'),('R'),('X');

CREATE TABLE climb_type(
	"type" TEXT PRIMARY KEY NOT NULL
);
INSERT INTO climb_type (type)
VALUES
	('boulder'),('TR'),('sport'),('trad'),('alpine ice'),('water ice'),('aid');

CREATE TABLE areas(
	"area_name" TEXT NOT NULL,
	"country" TEXT NOT NULL,
	"state" TEXT NOT NULL,
	"notes" TEXT,
	PRIMARY KEY("area_name", "state")
);
.mode csv
.import /home/andre/Documents/ticks-db/data/areas.csv areas

CREATE TABLE climbs(
	"name" TEXT NOT NULL,
	"grade" TEXT NOT NULL,
	"commitment" TEXT,
	"type" TEXT NOT NULL,
	"gps" TEXT NOT NULL,
	"area" TEXT NOT NULL,
	"area_state" TEXT NOT NULL,
	"notes" TEXT,
	FOREIGN KEY("area", "area_state") REFERENCES areas("area_name", "state"),
	PRIMARY KEY ("name", "area")
);
.mode csv
.import /home/andre/Documents/ticks-db/data/climbs.csv climbs

CREATE TABLE clients(
	"fname" TEXT NOT NULL,
    "lname" TEXT NOT NULL,
    "notes" TEXT,
    PRIMARY KEY ("fname", "lname")
);
.mode csv
.import /home/andre/Documents/ticks-db/data/clients.csv clients

CREATE TABLE ticks(
	"id" INTEGER PRIMARY KEY ASC,
	"date" TEXT NOT NULL,
	"name" TEXT NOT NULL,
	"area" TEXT NOT NULL,
	"pitches" INTEGER NOT NULL,
	"height" INTEGER NOT NULL,
	"style" TEXT NOT NULL,
	"lead_style" TEXT,
	"notes" TEXT,
	"client_fname" TEXT,
	"client_lname" TEXT,
	"partner_fname" TEXT,
	"partner_lname" TEXT,
	FOREIGN KEY("name", "area") REFERENCES climbs("name", "area"),
	FOREIGN KEY("client_fname", "client_lname") REFERENCES clients("fname", "lname")
);
.mode csv
.import /home/andre/Documents/ticks-db/data/ticks.csv ticks

CREATE TABLE guided(
	"date" TEXT NOT NULL,
	"client_fname" TEXT NOT NULL,
	"client_lname" TEXT NOT NULL,
	"company" TEXT NOT NULL,
	"tip" INTEGER,
	PRIMARY KEY ("date", "client_fname", "client_lname"),
	FOREIGN KEY("date") REFERENCES ticks("date"),
	FOREIGN KEY("client_fname", "client_lname") REFERENCES clients("fname", "lname")
);
.mode csv
.import /home/andre/Documents/ticks-db/training/guided.csv guided