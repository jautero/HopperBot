#!/bin/bash
. $HOME/.jautero.ems.host.env
git pull 
pipenv run python3 bot.py
