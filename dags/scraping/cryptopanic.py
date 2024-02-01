import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

USE_DOCKER_PROXY = os.getenv("USE_DOCKER_PROXY", "false") in ["true", "1"]
DOCKER_URL = (
    "tcp://docker-proxy:2375" if USE_DOCKER_PROXY else "unix://var/run/docker.sock"
)

with DAG(
    "scrap_cryptopanic",
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2023, 10, 20),
    catchup=False,
) as dag:
    run_scraper_task = DockerOperator(
        task_id="run_scraper_task",
        image="cryptodata-scraper:latest",
        api_version="auto",
        command="python main.py",
        docker_url=DOCKER_URL,
        network_mode="cryptodata_default",
        auto_remove="force",
        environment={"KAFKA_BROKER": "kafka:9092"},
    )
