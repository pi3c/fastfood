FROM python:3.10-slim

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN mkdir -p /usr/src/fastfood

WORKDIR /usr/src/fastfood

COPY ./pyproject.toml .

COPY ./poetry.lock .

RUN touch /usr/src/RUN_IN_DOCKER

RUN poetry install
