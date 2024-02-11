FROM apache/airflow:2.7.2-python3.11

COPY ./pyproject.toml ./poetry.lock ./

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install poetry redis

RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry install --only airflow --no-interaction --no-ansi --no-root \
    && . `poetry env info --path`/bin/activate
