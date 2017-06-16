from chatterbot import ChatBot
import yaml,os

config=yaml.load(file(os.path.expanduser(os.path.join("~",".HopperBot.yaml"))))

chatbot=ChatBot(me.username,
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database=config["database"])

chatterbot.set_trainer(ChatterBotCorpusTrainer)

chatterbot.train("chatterbot.corpus.english")
