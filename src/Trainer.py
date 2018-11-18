from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import yaml,os

config=yaml.load(file(os.path.expanduser(os.path.join("~",".HopperBot.yaml"))))

chatbot=ChatBot('Trainer',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database=config["database"])

chatbot.set_trainer(ChatterBotCorpusTrainer)

chatbot.train("chatterbot.corpus.english")
