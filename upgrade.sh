#!/bin/sh
. $HOME/venv/HopperBot/bin/activate
kill `cat hopperbot.pid`
git pull
python setup.py install
python YourHopperBot.py &
echo $! >hopperbot.pid