CREATE TABLE berichten(
	naam varchar(255) NOT NULL,
	bericht varchar(140) NOT NULL,
	datum date NOT NULL,
	tijd time NOT NULL,
	locatie varchar NOT NULL,
	goedgekeurd boolean NOT NULL,
	berichtid serial NOT NULL,
	moderatorid int NOT NULL,
	moddatum date NOT NULL,
	modtijd time NOT NULL,
	PRIMARY KEY (berichtid)
);

CREATE TABLE moderator(
	naam varchar(255) NOT NULL,
	emailadress varchar(255) NOT NULL,
	moderatorid serial NOT NULL,
	PRIMARY KEY (moderatorid)
);

CREATE TABLE station_service(
	station_city varchar(50) NOT NULL,
	country varchar(2) NOT NULL,
	ov_bike boolean NOT NULL,
	elevator boolean NOT NULL,
	toilet boolean NOT NULL,
	park_and_ride boolean NOT NULL,
	PRIMARY KEY (station_city)
);

ALTER TABLE berichten
ADD CONSTRAINT moderatorid
FOREIGN KEY (moderatorid)
REFERENCES moderator (moderatorid);

ALTER TABLE berichten
ADD CONSTRAINT stationid
FOREIGN KEY (locatie)
REFERENCES station_service (station_city);