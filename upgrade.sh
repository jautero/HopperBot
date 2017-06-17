#!/bin/sh
. $HOME/venv/HopperBot/bin/activate
kill `cat hopperbot.pid`
git pull
python setup.py install
python HopperBot.py &
echo $! >hopperbot.pid
