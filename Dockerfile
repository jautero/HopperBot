FROM python:3-alpine

RUN apk --update add build-base py3-cryptography

# pipenv is somewhat pointless in Docker container.
# RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app

RUN set -ex && pip install -vvv python-telegram-bot pyyaml chatterbot

COPY src/ ./
