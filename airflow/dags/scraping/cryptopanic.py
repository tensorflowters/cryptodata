import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable

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
    env = Variable.get("AIRFLOW_ENV", os.getenv('AIRFLOW_ENV', 'DEV'))

    if env == "PROD":
        # Use KubernetesPodOperator in production
        run_scraper_task = KubernetesPodOperator(
            task_id="run_cryptopanic_scraper_task",
            name="cryptopanic-scraper-task",
            namespace="default",
            image="epitechuser2077/cryptodata:cryptodata-cryptopanic-scraper",
            cmds=["python", "main.py"],
            env_vars={"KAFKA_BROKER": "kafka:9092", "GH_TOKEN": os.getenv("GH_TOKEN")},
            in_cluster=True,  # Assumes Airflow is running within a Kubernetes cluster
            get_logs=True,
            image_pull_policy="Always",
            is_delete_operator_pod=True,
        )
    else:
        run_scraper_task = DockerOperator(
            task_id="run_cryptopanic_scraper_task",
            image="epitechuser2077/cryptodata:cryptodata-cryptopanic-scraper",
            api_version="auto",
            command="python main.py",
            docker_url="tcp://docker-proxy:2375",  # Assumes a docker-proxy setup for local development
            network_mode="cryptodata_default",
            auto_remove=True,
            environment={"KAFKA_BROKER": "kafka:9092", "GH_TOKEN": os.getenv("GH_TOKEN")},
        )
