from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('scraper_cryptopanic',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5),  # Override to whatever interval you need
         start_date=datetime(2023, 10, 20),
         catchup=False) as dag:

    run_scraper_task = DockerOperator(
        task_id='run_scraper_task',
        image='scraper:latest',   # The name of the image you've built for the scraper
        api_version='auto',
        command="python main.py",  # or whatever command you need to run your scraper
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )
