import random, json, re, KeywordStore, StringIO
import logging
logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class HopperBot:
    def __init__(self,name):
        self.stockanswers=["A likely story!","I don't see what that has to do with anything!"]
        self.name=name
        self.memory=KeywordStore.KeywordStore()
        pinkydata=json.load(file("pinky.json"))
        self.pinkyquestions=set(q.format(name) for q in pinkydata["questions"])
        self.pinkyanswers=set(pinkydata["answers"])
    def process(self,msg):
        if msg.text == self.name + "!":
            return msg.name + "!"
        if msg.text == "dump memory":
            return self.dump_memory()
        if msg.text in self.pinkyquestions:
            return random.choice(list(self.pinkyanswers)).format(msg.name)
        try:
            return self.recall(re.sub('\W',' ',msg.text).lower().split()).pop()
        except IndexError:
            self.remember(msg.text)
            return random.choice(self.stockanswers)
    def remember(self,msg):
        tokens=re.sub('\W',' ',msg).lower().split()
        self.memory.store(msg,tokens)
    def recall(self,tokens):
        return self.memory.get(tokens)
    def dump_memory(self):
        stream=StringIO.StringIO()
        self.memory.dump(stream)
        return stream.getvalue()
