<strong>Weather project</strong>

<IMG SRC="diagram.jpg">

Dataset from NOAA (National Oceanic and Atmospheric Administration):
<BR>
https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/
<BR>
<BR>
<strong>Airflow</strong> has 2 DAG:
<BR>
1.<strong>data_ingestion.py</strong> (<A href="./airflow/dags/data_ingestion.py">source</A> in <A href="./airflow/dags">DAG folder</A>) - loading data from NOAA-database to local <strong>Postgres DB</strong>. The NOAA-database contains many archives by year. Each archives contain many files with data from different weather stations. The Postgres database contains tables for every year since 1929.
<BR>
2.<strong>data_ingestion_GC.py</strong> (<A href="./airflow/dags/data_ingestion_GC.py">source</A> in <A href="./airflow/dags">DAG folder</A>) - loading data from <strong>Postgres DB</strong> to <strong>Google BigQuery</strong>. In Google BigQuery there is only one partitioned (by date) table "day_stat_part_date".
<BR>
<BR>  
Dashboard developed in Dash Python (<A href="./dash">dash folder</A>). The application was dockerized and uploaded to AWS Elastic Beanstalk.<BR>
<strong>Demonstration version:</strong><BR>
http://weatherworld.us-east-2.elasticbeanstalk.com/
<BR>
This application query data from Google BigQuery.
<BR><BR>
<strong>How to start:</strong><BR>
1.Make network:<BR>
docker network airflow_default<BR>
2.Start Postgres with PGAdmin:<BR>
docker compose docker-compose.yaml<BR>
3.Start Airflow:<BR>
docker airflow/compose docker-compose.yaml<BR>
4.Start demonstration application from http://weatherworld.us-east-2.elasticbeanstalk.com/ or manually:<BR>
python dash/app/main.py
