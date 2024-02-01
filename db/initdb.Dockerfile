FROM python:3.10.13-alpine3.18


RUN apk update \
    && apk add --no-cache gcc musl-dev libffi-dev openssl-dev

RUN mkdir /srv/app
WORKDIR /srv/app

COPY ./db .

RUN pip install --upgrade pip
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only db --no-interaction --no-ansi --no-root
