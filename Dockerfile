FROM python:3.8

COPY . .

RUN pip install poetry
RUN poetry update
