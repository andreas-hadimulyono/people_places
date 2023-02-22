CREATE DATABASE people_places;

use people_places;

CREATE TABLE people (
  given_name VARCHAR(50),
  family_name VARCHAR(50),
  date_of_birth DATE,
  place_of_birth VARCHAR(50)
);

CREATE TABLE places (
  city VARCHAR(50),
  county VARCHAR(50),
  country VARCHAR(50)
);
