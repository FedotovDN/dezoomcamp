# dezoomcamp
docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v C:/Users/fedot/Desktop/DECourse/week1/pg_data:/var/lib/postgresql/data -p 5432:5432 --network=pg-network --name pg-database postgres:13

docker run -it -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" -e PGADMIN_DEFAULT_PASSWORD="root" -p 8080:80 --network=pg-network --name pgadmin-2 dpage/pgadmin4

URL="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"

python ingest_data.py --user=root --password=root --host=localhost --port=5432 --db=ny_taxi --table_name=yellow_taxi_trips --url=https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv

<b>Question 3. Count records</b>
<br>
SELECT count(index)
FROM yellow_taxi_trips
WHERE tpep_pickup_datetime >= '2021-01-15' and tpep_pickup_datetime < '2021-01-16'

<b>Question 4. Largest tip for each day</b>
<br>
SELECT *
FROM yellow_taxi_trips
WHERE tip_amount = (select max(tip_amount) from yellow_taxi_trips)

<b>Question 5. Most popular destination</b>
<br>
SELECT z2."Borough", z2."Zone", count(t.*) cnt
FROM yellow_taxi_trips t,
     taxi_zone z1,
	 taxi_zone z2
WHERE z1."LocationID" = t."PULocationID" 
  AND z2."LocationID" = t."DOLocationID"
  AND t.tpep_pickup_datetime >= '2021-01-14' 
  AND t.tpep_pickup_datetime < '2021-01-15' 
  AND t."PULocationID" = 43
GROUP BY z2."Borough", z2."Zone"
ORDER BY cnt desc
LIMIT 1

<b>Question 6. Most expensive locations</b>
<br>
select z1."Borough", z1."Zone", z2."Borough", z2."Zone", avg(t."total_amount") ta
from yellow_taxi_trips t, taxi_zone z1, taxi_zone z2
where t."PULocationID" = z1."LocationID" 
  and t."DOLocationID" = z2."LocationID"
Group by z1."Borough", z1."Zone", z2."Borough", z2."Zone"
order by ta desc
LIMIT 1
