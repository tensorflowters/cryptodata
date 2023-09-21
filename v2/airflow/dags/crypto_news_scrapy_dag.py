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
    'crypto_news_scrapy_dag',
    default_args=default_args,
    description='Run Scrapy to scrape crypto news every 5 minutes',
    schedule_interval=timedelta(minutes=5),  # Override to whatever interval you need
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Task to run Scrapy spider
t1 = BashOperator(
    task_id='run_scrapy',
    bash_command='cd /path/to/your/scrapy/project && scrapy crawl cryptopanic',
    dag=dag,
)
