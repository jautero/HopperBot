#!/usr/bin/env python
#This is your bot configuration.
import HopperBot
import TelegramAPI
import os, yaml

config=yaml.load(file(os.path.expanduser(os.path.join("~",".HopperBot.yaml"))))

bot=HopperBot.HopperBot()
api=TelegramAPI.API(bot,config.telegram.apikey)
while True:
    pass