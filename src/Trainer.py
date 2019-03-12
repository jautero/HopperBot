from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import yaml,os

config=yaml.load(open(os.path.join("/app/config","HopperBot.yaml")))

chatbot=ChatBot('Trainer',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri=config["database_uri"])

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("chatterbot.corpus.english")
