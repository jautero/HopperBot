from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from chatterbot import ChatBot
import yaml, os
import logging

def handle_user_id(bot, update):
    update.message.reply_text(
        "You are {}".format(update.message.from_user.id))

def handle_chatbot(bot, update):
    update.message.reply_text(bot.chatbot.get_response(update.message.text))

def register_handlers(updater):
    updater.dispatcher.add_handler(CommandHandler("id",handle_user_id))
    updater.dispatcher.add_handler(MessageHandler(Filters.text,handle_chatbot))

logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    config=yaml.load(file(os.path.expanduser(os.path.join("~",".HopperBot.yaml"))))
    updater=Updater(config["telegram"]["apikey"])
    me=updater.get_me()
    updater.chatbot=ChatBot(me.username,
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database=config["database"])
    register_handlers(updater)
    updater.start_polling()
    updater.idle()
