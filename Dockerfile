FROM python:3-alpine

RUN set -ex && pip install ${PIP_ARGS} --upgrade python-telegram-bot matrix-client

RUN git clone https://github.com/shawnanastasio/python-matrix-bot-api.git \
    && cd python-matrix-bot-api && python setup.py install

RUN rm -rf python-matrix-bot-api

COPY src/*.py /app/
