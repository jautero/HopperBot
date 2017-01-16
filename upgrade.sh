#!/bin/sh
. $HOME/virtenv/HopperBot/bin/activate
git pull
python setup.py install
