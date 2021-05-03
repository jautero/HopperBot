#!/bin/bash
. $HOME/.jautero.ems.host.env
git pull
pipenv install
pipenv run python3 bot.py
