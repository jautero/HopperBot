from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from chatterbot import ChatBot
import yaml, os
import logging

def handle_user_id(bot, update):
    update.message.reply_text(
        "You are {}".format(update.message.from_user.id))

def handle_chatbot(bot, update):
    update.message.reply_text(bot.chatbot.get_response(update.message.text).text)

def handle_voice(bot, update):
    logging.info(update.message.voice)
    update.message.reply_text("You sent voice!")

def register_handlers(updater):
    updater.dispatcher.add_handler(CommandHandler("id",handle_user_id))
    updater.dispatcher.add_handler(MessageHandler(Filters.text,handle_chatbot))
    updater.dispatcher.add_handler(MessageHandler(Filters.voice,handle_voice))

logging.basicConfig(filename="/app/HopperBot.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    config=yaml.load(open(os.path.join("/app/config","HopperBot.yaml")))
    updater=Updater(config["telegram"]["apikey"])
    me=updater.bot.get_me()
    updater.bot.chatbot=ChatBot(me.username,
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        notes_store='mongo_note_store.MongoNoteStore',
        logic_adapters=['notes_adapter.NotesAdapter',
            "chatterbot.logic.BestMatch"],
        database=config["database"], database_uri=config["database_uri"])
    register_handlers(updater)
    updater.start_polling()
    updater.idle()
