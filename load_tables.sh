#!/bin/bash

mysql -uroot -ppassword people_places -e "LOAD DATA LOCAL INFILE '/tmp/people.csv' INTO TABLE people FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"
mysql -uroot -ppassword people_places -e "LOAD DATA LOCAL INFILE '/tmp/places.csv' INTO TABLE places FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"

