#!/bin/sh
cd /srv/HopperBot
CONTAINER_ID=`cat container.id`
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID
docker run -d -v $PWD/config:/app/config jautero/hopperbot python HopperBot.py >container.id
