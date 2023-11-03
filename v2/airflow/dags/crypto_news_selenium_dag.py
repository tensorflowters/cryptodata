from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'crypto_news_selenium_dag',
    default_args=default_args,
    description='Run Selenium to scrape crypto news every 5 minutes',
    schedule_interval=timedelta(minutes=5),  # Override to whatever interval you need
    start_date=datetime(2023, 4, 10),
    catchup=False,
)

t1 = BashOperator(
    task_id='run_selenium',
    bash_command='cd /opt/bitnami/airflow/dags && ./start.sh',
    dag=dag,
)
