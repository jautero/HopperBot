FROM python:3-alpine

RUN apk --update add build-base py-cryptography

# pipenv is somewhat pointless in Docker container.
# RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app

RUN set -ex && pip install pyyaml chatterbot

COPY src /app/
