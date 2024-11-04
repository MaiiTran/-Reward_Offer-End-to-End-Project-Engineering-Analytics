from airflow import DAG
from datetime import date, datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from reward_offer_etl import etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,10,6),
    'retries': 2,
    'retry_delay': timedelta(minutes = 5),

}

dag = DAG(
    'reward_offer_dag',
    default_args = default_args,
    description = 'Dag with ETL process',
    schedule_interval = timedelta(days=1)
)

run_etl = PythonOperator (
    task_id = 'complete_reward_offer_etl',
    python_callable = etl,
    dag = dag
)

run_etl
