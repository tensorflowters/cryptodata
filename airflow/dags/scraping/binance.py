import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "conditional_operator_example",
    default_args=default_args,
    schedule_interval=timedelta(minutes=2),
    start_date=datetime(2023, 10, 20),
    catchup=False,
)

# Get the environment setting (prod or dev)
# First try to get it from Airflow Variable, fallback to OS environment variable
env = Variable.get("AIRFLOW_ENV", os.getenv("AIRFLOW_ENV", "DEV"))

if env == "PROD":
    task = KubernetesPodOperator(
        task_id="run_in_k8s",
        name="k8s-task",
        namespace="default",
        image="epitechuser2077/cryptodata:cryptodata-binance-scraper",
        cmds=["python", "main.py"],
        env_vars={"KAFKA_BROKER": "kafka:9092", "GH_TOKEN": os.getenv("GH_TOKEN")},
        dag=dag,
        in_cluster=True,
        get_logs=True,
    )
else:  # dev environment
    task = DockerOperator(
        task_id="run_in_docker",
        image="epitechuser2077/cryptodata:cryptodata-binance-scraper",
        api_version="auto",
        command="python main.py",
        environment={"KAFKA_BROKER": "kafka:9092", "GH_TOKEN": os.getenv("GH_TOKEN")},
        dag=dag,
    )
