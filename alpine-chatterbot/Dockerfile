FROM python:3-alpine

RUN apk update && apk add --no-cache gcc mailcap python3-dev build-base py-numpy py3-cryptography linux-headers pcre-dev postgresql-dev libffi-dev cython libressl-dev

# pipenv is somewhat pointless in Docker container.
# RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app

RUN set -ex && pip install ${PIP_ARGS} --upgrade pip chatterbot 
