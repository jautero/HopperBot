FROM python:3-alpine

RUN apk update && apk add --no-cache gcc git mailcap python3-dev build-base py-numpy py3-cryptography linux-headers pcre-dev postgresql-dev libffi-dev libressl-dev

# pipenv is somewhat pointless in Docker container.
# RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app


RUN set -ex && pip install ${PIP_ARGS} --upgrade pip Cython
RUN set -ex && pip install ${PIP_ARGS} --upgrade chatterbot 
RUN set -ex && pip install ${PIP_ARGS} --upgrade chatterbot_corpus
