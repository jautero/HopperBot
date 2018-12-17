FROM python:3-alpine

RUN apk --update add build-base libffi-dev openssl-dev python-dev py-pip
RUN pip install --no-cache-dir cryptography

# pipenv is somewhat pointless in Docker container.
# RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app

RUN set -ex && pip install python-telegram-bot pyyaml chatterbot

COPY src/ ./
