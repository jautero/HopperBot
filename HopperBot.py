from telegram.ext import Updater, CommandHandler
import yaml, os
import logging

def handle_user_id(bot, update):
    update.message.reply_text(
        "You are {}".format(update.message.from_user.id))

def register_handlers(updater):
    updater.dispatcher.add_handler(CommandHandler("id",handle_user_id))

logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    config=yaml.load(file(os.path.expanduser(os.path.join("~",".HopperBot.yaml"))))
    updater=Updater(config["telegram"]["apikey"])

    register_handlers(updater)
    updater.start_polling()
    updater.idle()
