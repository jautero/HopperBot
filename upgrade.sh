#!/bin/sh
. $HOME/venv/HopperBot/bin/activate
git pull
python setup.py install
