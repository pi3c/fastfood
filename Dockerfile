FROM python:3.10-slim

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN mkdir -p /usr/src/fastfood

WORKDIR /usr/src/fastfood

COPY ./example.env .

COPY ./poetry.lock .

COPY ./pyproject.toml .

RUN touch /usr/src/RUN_IN_DOCKER

RUN poetry install
