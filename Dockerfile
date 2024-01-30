FROM python:3.10-slim

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN mkdir -p /usr/src/fastfood

WORKDIR /usr/src/fastfood

COPY . .

RUN poetry install
