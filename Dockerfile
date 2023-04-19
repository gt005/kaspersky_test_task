FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /kaspersky_app

COPY requirements.txt /kaspersky_app/
COPY supervisord.conf /kaspersky_app/

RUN pip install -r requirements.txt
RUN pip install supervisor

COPY . /kaspersky_app/
