DROP TABLE IF EXISTS nursing_home_quality;

DROP TABLE IF EXISTS facility;

DROP TABLE IF EXISTS measurment;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS userlogs;

DROP DATABASE IF EXISTS nursing_home;

DROP SCHEMA IF EXISTS testing CASCADE;

DROP USER IF EXISTS nursing_home;

CREATE DATABASE nursing_home;
CREATE USER nursing_home WITH PASSWORD 'nursing_home';
GRANT ALL PRIVILEGES ON DATABASE nursing_home TO nursing_home;


CREATE SCHEMA testing;
ALTER USER admin SET search_path = testing;
GRANT ALL PRIVILEGES ON SCHEMA testing TO nursing_home;



create table facility (

facility_id SMALLINT PRIMARY KEY,
facility_name VARCHAR (200) NOT NULL,
current_facility_name VARCHAR(200),
facility_OPCERT INT,
faclity_medicare_number INT,
city VARCHAR (30),
county VARCHAR (30),
region VARCHAR (30),
location POINT
	
);

create table measurment (

measure_id_number NUMERIC PRIMARY KEY,
measure_short_name VARCHAR(50),
measure_full_name VARCHAR(200)
	
);


create table nursing_home_quality(

measure_id_number NUMERIC,
facility_id SMALLINT,
first_quintile REAL,
second_quintile REAL,
third_quintile REAL,
fourth_quintile REAL,
fifth_quintile REAL,
numeric_value REAL,
character_value CHAR(5),
quintile VARCHAR(5),
points SMALLINT,
measurement_year INT,
comments VARCHAR(255),
nursing_home_quality_id INT,
PRIMARY KEY(nursing_home_quality_id),
CONSTRAINT fk_faciltiy
	FOREIGN KEY(facility_id)
		REFERENCES facility(facility_id) ON UPDATE CASCADE ON DELETE CASCADE,
	
CONSTRAINT fk_measurement
	FOREIGN KEY(measure_id_number)
		REFERENCES measurment(measure_id_number) ON UPDATE CASCADE ON DELETE CASCADE
);



create table users(

userid BIGINT PRIMARY KEY,
password VARCHAR(20),
email VARCHAR(30),
notes VARCHAR(500)	
);

create table userlogs(

userid VARCHAR(50) NOT NULL,
tablename VARCHAR(50) NOT NULL,
time TIMESTAMP,
querylog VARCHAR(2000) NOT NULL
);

GRANT ALL PRIVILEGES ON TABLE facility TO nursing_home;
GRANT ALL PRIVILEGES ON TABLE measurment TO nursing_home;
GRANT ALL PRIVILEGES ON TABLE nursing_home_quality TO nursing_home;
GRANT ALL PRIVILEGES ON TABLE users TO nursing_home;
GRANT ALL PRIVILEGES ON TABLE userlogs TO nursing_home;

