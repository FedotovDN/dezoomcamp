import os

from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_script_fhv import ingest_callable


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')


local_workflow = DAG(
    "LocalIngestionDagFHV",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2019, 1, 1)
)

URL_PREFIX = 'https://nyc-tlc.s3.amazonaws.com/trip+data' 
URL_TEMPLATE = URL_PREFIX + '/fhv_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_fhv_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
TABLE_NAME_TEMPLATE = 'fhv_{{ execution_date.strftime(\'%Y_%m\') }}'

with local_workflow:
    wget_task = BashOperator(
        task_id='wget',
        bash_command=f'curl -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}'
    )

    ingest_task = PythonOperator(
        task_id="ingest_fhv",
        python_callable=ingest_callable,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=TABLE_NAME_TEMPLATE,
            csv_file=OUTPUT_FILE_TEMPLATE
        ),
    )

    wget_task >> ingest_task