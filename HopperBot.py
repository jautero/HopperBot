from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from chatterbot import ChatBot
import yaml, os
import logging

def handle_user_id(bot, update):
    update.message.reply_text(
        "You are {}".format(update.message.from_user.id))

def handle_chatbot(bot, update):
    update.message.reply_text(bot.chatbot.get_response(update.message.text).text)

def handle_audio(bot, update):
    logging.info(update.message.audio)
    update.message.reply_text("You sent audio!")

def register_handlers(updater):
    updater.dispatcher.add_handler(CommandHandler("id",handle_user_id))
    updater.dispatcher.add_handler(MessageHandler(Filters.text,handle_chatbot))
    updater.dispatcher.add_handler(MessageHandler(Filters.audio,handle_audio))

logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    config=yaml.load(file(os.path.expanduser(os.path.join("~",".HopperBot.yaml"))))
    updater=Updater(config["telegram"]["apikey"])
    me=updater.bot.get_me()
    updater.bot.chatbot=ChatBot(me.username,
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database=config["database"])
    register_handlers(updater)
    updater.start_polling()
    updater.idle()
