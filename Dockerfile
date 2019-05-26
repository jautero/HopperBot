FROM python:3-alpine

RUN apk update && apk add --no-cache gcc mailcap python3-dev build-base py-numpy py3-cryptography linux-headers pcre-dev postgresql-dev libffi-dev libressl-dev

# pipenv is somewhat pointless in Docker container.
# RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app

RUN set -ex && pip install --upgrade pip pyyaml pytz boto3 
RUN set -ex && pip install --upgrade numpy cryptography
RUN set -ex && pip install --upgrade python-telegram-bot chatterbot matrix-client

RUN git clone https://github.com/shawnanastasio/python-matrix-bot-api.git \
    && cd python-matric-bot-api && python setup.py install

RUN rm -rf python-matrix-bot-api

COPY src/*.py /app/
