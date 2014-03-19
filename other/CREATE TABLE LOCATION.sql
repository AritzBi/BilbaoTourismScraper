#Pasos para instalar
# brew install postgresql
#Ejecutar despuues de instalar
#ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
#launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist
#Or, if you don't want/need launchctl, you can just run:
#   postgres -D /usr/local/var/postgres
#Crear db-->createdb mydb
#psql mydb --> Para acceder a ese schema
#\d+           Show all tables, with descriptions
#\d+ table     Show the definition of the named table (or view), with  column descriptions
#\?            Describe briefly all the \ commands in psql               


CREATE TABLE EVENT_TYPE
(ID SERIAL PRIMARY KEY,
DENOM VARCHAR(255)
);



CREATE TABLE EVENT_SUBTYPE
(ID SERIAL PRIMARY KEY,
DENOM VARCHAR(255),
TYPE_ID INTEGER references event_type(id)
);

CREATE TABLE LOCATION
(ID SERIAL PRIMARY KEY,
ADDRESS VARCHAR(255),
geom GEOMETRY(Point, 4326),
UNIQUE (ADDRESS));

CREATE TABLE HOSTELERY_TYPE
(ID SERIAL PRIMARY KEY,
FIRST_TYPE_ES VARCHAR(255),
SECOND_TYPE_ES VARCHAR(255),
FIRST_TYPE_EU VARCHAR(255),
SECOND_TYPE_EU VARCHAR(255),
FIRST_TYPE_EN VARCHAR(255),
SECOND_TYPE_EN VARCHAR(255)
);

CREATE TABLE HOSTELERY
(ID SERIAL PRIMARY KEY,
DENOM_ES VARCHAR(255),
DENOM_EU VARCHAR(255),
DENOM_EN VARCHAR(255),
LOCATION_ID INTEGER references location(id),
DESCRIPTION_ES VARCHAR(1000),
DESCRIPTION_EU VARCHAR(1000),
DESCRIPTION_EN VARCHAR(1000),
INFORMATION_URL VARCHAR(255),
HOSTELERY_TYPE INTEGER references hostelery_type(id),
TELEPHONE VARCHAR(255),
EMAIL VARCHAR(255)
);

CREATE TABLE EVENT
(ID SERIAL PRIMARY KEY,
DENOM VARCHAR(255),
INFORMATION_URL VARCHAR(255),
STARTDATE DATE,
ENDATE DATE,
STARTHOUR VARCHAR(255),
ENDHOUR VARCHAR(255),
TYPE_ID INTEGER references event_subtype(id),
PRICE VARCHAR(255),
RANGE_PRICES BOOLEAN
);

CREATE TABLE EVENT_LOCATION 
(
LOCATION_ID INTEGER references location(id),
DENOM VARCHAR(255),
EVENT_ID INTEGER references event(id),
PRIMARY KEY(LOCATION_ID, EVENT_ID)
); 

CREATE TABLE BUILDING_TYPE
(ID SERIAL PRIMARY KEY,
DENOM_ES VARCHAR(255),
DENOM_EU VARCHAR(255),
DENOM_EN VARCHAR(255)
);

CREATE TABLE EMBLEMATIC_BUILDING
(ID SERIAL PRIMARY KEY,
DENOM_ES VARCHAR(255),
DENOM_EU VARCHAR(255),
DENOM_EN VARCHAR(255),
LOCATION_ID INTEGER references location(id),
DESCRIPTION_ES VARCHAR(2000),
DESCRIPTION_EU VARCHAR(2000),
DESCRIPTION_EN VARCHAR(2000),
INFORMATION_URL VARCHAR(255),
BUILDING_TYPE INTEGER references building_type(id)
);

CREATE TABLE MEMBER
(ID SERIAL PRIMARY KEY,
USERNAME VARCHAR(255),
SALT VARCHAR(255),
HASH VARCHAR(255),
NAME VARCHAR(255),
SURNAME VARCHAR(255),
UNIQUE(USERNAME)
);

INSERT INTO event_type(denom) VALUES ('Infantiles');
INSERT INTO event_type(denom) VALUES ('Exposiciones');
INSERT INTO event_type(denom) VALUES ('Concursos');
INSERT INTO event_type(denom) VALUES ('Jornadas, conferencias y congresos');
#Voy a meter Opera tambien aqui.
INSERT INTO event_type(denom) VALUES ('Música');
INSERT INTO event_type(denom) VALUES ('Teatro y Danza');
INSERT INTO event_type(denom) VALUES ('Cine');
INSERT INTO event_type(denom) VALUES ('Deportes');
INSERT INTO event_type(denom) VALUES ('Mercados y compras');
INSERT INTO event_type(denom) VALUES ('Folclore y fiestas populares');
INSERT INTO event_type(denom) VALUES ('Otros');