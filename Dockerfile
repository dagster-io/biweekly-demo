FROM python:3.8-slim

RUN apt update && apt install -y python3-lxml
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /opt/dagster/app

COPY . /opt/dagster/app