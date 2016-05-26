import random, json, re, KeywordStore

class HopperBot:
    def __init__(self,name):
        self.stockanswers=["A likely story!","I don't see what that has to do with anything!"]
        self.name=name
        self.memory=KeywordStore.KeywordStore()
        pinkydata=json.load(file("pinky.json"))
        self.pinkyquestions=set(q.format(name) for q in pinkydata["questions"])
        self.pinkyanswers=set(pinkydata["answers"])
    def process(self,nick,msg):
        if msg == self.name + "!":
            return nick + "!"
        if msg in self.pinkyquestions:
            return random.choice(list(self.pinkyanswers)).format(nick)
        try:
            return self.recall(re.sub('\W',' ',msg).lower.split()).pop()
        except: 
            self.remember(msg)
            return random.choice(self.stockanswers)
    def remember(self,msg):
        tokens=re.sub('\W',' ',msg).lower().split()
        self.memory.store(msg,tokens)
    def recall(self,tokens):
        return self.memory.get(tokens)