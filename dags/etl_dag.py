import requests
from configparser import ConfigParser
import json
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import date, timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

from get_menu import get_menu
from read_recipes import read_recipes
from upload_to_s3 import upload_to_s3


# initialize logger
logging.basicConfig(filename='../logs/weekly_menu_etl.log', level=logging.DEBUG, force=True)


# initialize and read configurations
cp = ConfigParser()
cp.read("config.ini")

retries = int(cp["dag"]["retries"])
retry_delay = int(cp["dag"]["retry_delay"])
start_day_delay = int(cp["dag"]["start_day_delay"])
schedule_interval = cp["dag"]["schedule_interval"]


# extract year and week 
today = date.today()
year = today.year
week = today.isocalendar()[1]
    

# default params for DAG
default_args = {
    'owner': 'sadari',
    'depends_on_past': True,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=retry_delay)
}


# DAG for weekly menu ETL
with DAG('weekly_menu_dag',
         default_args = default_args,
         description ='ETL pipeline for Weekly Menu',
         start_date = days_ago(start_day_delay),
         schedule_interval = schedule_interval,
         max_active_runs = 1,
         catchup = False
) as dag:

    extract = PythonOperator(
        task_id = 'extract_menu',
        python_callable = get_menu,
        op_kwargs={'year': year, 'week': week}
    )

    transform = PythonOperator(
        task_id ='transform_recipes',
        python_callable = read_recipes,
        op_kwargs = {'year': year, 'week': week}
    )

    load = PythonOperator(
        task_id ='load_recipes',
        python_callable = upload_to_s3,
        op_kwargs = {'year': year, 'week': week}
    )

    extract >> transform >> load
