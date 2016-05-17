import random, json

class HopperBot:
    def __init__(self,name):
        self.stockanswers=["A likely story!","I don't see what that has to do with anything!"]
        self.name=name
        pinkydata=json.load(file("pinky.json"))
        self.pinkyquestions=set(q.format(name) for q in pinkydata["questions"])
        self.pinkyanswers=set(pinkydata["answers"])
    def process(self,nick,msg):
        if msg in self.pinkyquestions:
            return random.choice(list(self.pinkyanswers)).format(nick)
        return random.choice(self.stockanswers)