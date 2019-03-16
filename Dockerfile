FROM python:3-alpine

RUN apk add --no-cache gcc mailcap python3-dev build-base linux-headers pcre-dev postgresql-dev libffi-dev libressl-dev

# pipenv is somewhat pointless in Docker container.
# RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app

RUN set -ex && pip install --upgrade pip python-telegram-bot pyyaml pytz chatterbot boto3

COPY src/*.py /app/
