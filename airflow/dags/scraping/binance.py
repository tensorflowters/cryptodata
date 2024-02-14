import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "scrap_binance",
    default_args=default_args,
    schedule_interval=timedelta(minutes=2),
    start_date=datetime(2023, 10, 20),
    catchup=False,
) as dag:
    env = Variable.get("AIRFLOW_ENV", os.getenv("AIRFLOW_ENV", "DEV"))

    if env == "PROD":
        task = KubernetesPodOperator(
            task_id="run_binance_scraper_task",
            name="binance_scraper_task",
            namespace="default",
            image="epitechuser2077/cryptodata:cryptodata-binance-scraper",
            cmds=["python", "main.py"],
            env_vars={"KAFKA_BROKER": "kafka:9092", "GH_TOKEN": os.getenv("GH_TOKEN")},
            in_cluster=True,  # Assumes Airflow is running within a Kubernetes cluster
            get_logs=True,
            image_pull_policy="Always",
            is_delete_operator_pod=True,
        )
    else:  # dev environment
        task = DockerOperator(
            task_id="run_binance_scraper_task",
            image="epitechuser2077/cryptodata:cryptodata-binance-scraper",
            api_version="auto",
            command="python main.py",
            environment={
                "KAFKA_BROKER": "kafka:9092",
                "GH_TOKEN": os.getenv("GH_TOKEN"),
            },
            network_mode="cryptodata_default",
            auto_remove="force",
            docker_url="tcp://docker-proxy:2375",
        )
