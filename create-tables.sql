PRAGMA foreign_keys = OFF;
DROP TABLE IF EXISTS guided;
DROP TABLE IF EXISTS ticks;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS climbs;
DROP TABLE IF EXISTS areas;

CREATE TABLE areas(
	"area_name" TEXT NOT NULL PRIMARY KEY,
	"country" TEXT NOT NULL,
	"state" TEXT NOT NULL,
	"notes" TEXT
);
.mode csv
.import /home/andre/Documents/ticks-db/training/areas.csv areas

CREATE TABLE climbs(
	"name" TEXT NOT NULL,
	"grade" TEXT NOT NULL,
	"commitment" TEXT,
	"type" TEXT NOT NULL,
	"gps" TEXT NOT NULL,
	"area" TEXT NOT NULL,
	FOREIGN KEY("area") REFERENCES areas("area_name"),
	PRIMARY KEY ("name", "area")
);
.mode csv
.import /home/andre/Documents/ticks-db/training/climbs.csv climbs

CREATE TABLE clients(
	"fname" TEXT NOT NULL,
    "lname" TEXT NOT NULL,
    "notes" TEXT,
    PRIMARY KEY ("fname", "lname")
);
.mode csv
.import /home/andre/Documents/ticks-db/training/clients.csv clients

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
	FOREIGN KEY("name", "area") REFERENCES climbs("name", "area"),
	FOREIGN KEY("client_fname", "client_lname") REFERENCES clients("fname", "lname")
);
.mode csv
.import /home/andre/Documents/ticks-db/training/ticks.csv ticks

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