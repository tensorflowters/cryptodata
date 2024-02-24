import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    "scrap_cryptopanic",
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2023, 10, 20),
    catchup=False,
) as dag:
    # Determine the environment; default to 'dev' if not specified
    env = Variable.get("AIRFLOW_MODE", os.getenv("AIRFLOW_MODE", "dev"))

    if env == "prod":
        run_scraper_task = DockerOperator(
            api_version="auto",
            auto_remove="force",
            command="python main.py",
            docker_url="tcp://docker-proxy:2375",
            environment={
                "AIRFLOW_GH_TOKEN": os.getenv("AIRFLOW_GH_TOKEN"),
                "KAFKA_BROKER": "kafka:9092",
            },
            image="epitechuser2077/cryptodata:cryptodata-cryptopanic-scraper",
            network_mode="cryptodata_net",
            task_id="run_cryptopanic_scraper_task",
        )
    else:
        run_scraper_task = DockerOperator(
            api_version="auto",
            auto_remove="force",
            command="python main.py",
            docker_url="tcp://docker-proxy:2375",  # Assumes a docker-proxy setup for local development
            environment={
                "AIRFLOW_GH_TOKEN": os.getenv("AIRFLOW_GH_TOKEN"),
                "KAFKA_BROKER": "kafka:9092",
            },
            image="cryptodata-cryptopanic-scraper:latest",
            network_mode="cryptodata_net",
            task_id="run_cryptopanic_scraper_task",
        )
