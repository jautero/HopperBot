FROM python:3-alpine

RUN apk add build-base 

RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app

RUN set -ex && pipenv install python-telegram-bot pyyaml chatterbot

COPY src/ ./
