FROM python:3.10-slim

RUN mkdir /fastfood

WORKDIR /fastfood

COPY . .

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

RUN chmod a+x scripts/*.sh
