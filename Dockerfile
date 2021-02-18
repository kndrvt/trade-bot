FROM python:3.8

COPY . .

RUN pip install pyyaml
RUN pip install websockets