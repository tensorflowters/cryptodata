FROM apache/airflow:2.7.2-python3.11

# Switching to the root user to install packages
USER airflow

COPY airflow-requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

