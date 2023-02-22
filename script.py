import os
import mysql.connector
import pandas as pd
import json
import time

# this could possibly start before mysqld finished, so make simple retry
# to connect before proceeding. in ideal world, the mysql should have healthcheck
mydb = None
cursor = None
attempts = 0
while attempts < 3:
    try:
        mydb = mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            port=os.environ['MYSQL_PORT'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DB']
        )
        cursor = mydb.cursor()
        break
    except:
        attempts += 1
        print('unable to connect, waiting for a few seconds before trying again')
        time.sleep(5)

print('Loading Data')

# load people data
people_data = pd.read_csv('/data/people.csv', index_col=False, delimiter=',')
people_data.info()

for i, row in people_data.iterrows():
    sql = "INSERT INTO people(given_name, family_name, date_of_birth, place_of_birth) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))

# load places data
places_data = pd.read_csv('/data/places.csv', index_col=False, delimiter=',')
places_data.info()

for i, row in places_data.iterrows():
    sql = "INSERT INTO places(city, county, country) VALUES (%s,%s,%s)"
    cursor.execute(sql, tuple(row))

mydb.commit()

# generate output
generate_output_query = """WITH country_list as (
  select country from places group by country
),
people_country as (
  select
    places.country,
    count(1) as country_count
  from people
    left join places on people.place_of_birth = places.city
  group by 1
)
select
  country_list.country,
  IFNULL(country_count, 0) as country_count
from country_list
  left join people_country on country_list.country = people_country.country"""

cursor.execute(generate_output_query)
rows = cursor.fetchall()
json_data = {}

for r in rows:
    json_data[r[0]] = r[1]

print(json_data)

with open('/data/summary_output.json', 'w') as f:
    json.dump(json_data, f)

# to keep the container running, so that we can see the sample_output file
while True:
    time.sleep(1000)