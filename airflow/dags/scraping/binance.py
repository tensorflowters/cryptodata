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
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    "scrap_binance",
    default_args=default_args,
    schedule_interval=timedelta(minutes=2),
    start_date=datetime(2023, 10, 20),
    catchup=False,
) as dag:
    env = Variable.get("AIRFLOW_MODE", os.getenv("AIRFLOW_MODE", "dev"))

    if env == "prod":
        task = DockerOperator(
            task_id="run_binance_scraper_task",
            image="epitechuser2077/cryptodata:cryptodata-binance-scraper",
            api_version="auto",
            command="python main.py",
            environment={
                "KAFKA_BROKER": "kafka:9092",
                "GH_TOKEN": os.getenv("AIRFLOW_GH_TOKEN"),
            },
            network_mode="cryptodata_net",
            auto_remove="force",
            docker_url="tcp://docker-proxy:2375",
        )
    else:  # dev environment
        task = DockerOperator(
            task_id="run_binance_scraper_task",
            image="cryptodata-binance-scraper:latest",
            api_version="auto",
            command="python main.py",
            environment={
                "KAFKA_BROKER": "kafka:9092",
                "GH_TOKEN": os.getenv("AIRFLOW_GH_TOKEN"),
            },
            network_mode="cryptodata_net",
            auto_remove="force",
            docker_url="tcp://docker-proxy:2375",
        )
