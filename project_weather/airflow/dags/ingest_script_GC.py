from time import time
import pandas as pd
from google.cloud import bigquery
from sqlalchemy import create_engine

project_id = 'scweb-325801'
client = bigquery.Client.from_service_account_json('/opt/airflow/dags/scweb-325801-a43f2038549f.json')


def ingest_callable(user, password, host, port, db, table_name, year, execution_date):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    print('connection established successfully, instering data...')

    t_start = time()
    df = pd.read_sql(f'select * from day_stat_{year}', engine)
    df.STATION = df.STATION.astype(str)
    df.NAME = df.NAME.astype(str)
    df.DATE = pd.to_datetime(df.DATE)
    df.drop('index', axis=1, inplace=True)

    dataset_ref = client.dataset('weather_fdn') 
    table_ref = dataset_ref.table(table_name)
    result = client.load_table_from_dataframe(df, table_ref).result()

    t_end = time()

    print('inserted, took %.3f second' % (t_end - t_start))
