import random

class HopperBot:
    def __init__(self):
        self.stockanswers=["A likely story!","I don't see what that has to do with anything!"]
    def process(self,msg):
        if msg == "Are you pondering what I'm pondering?":
            return "Poit, I guess I am."
        return random.choice(self.stockanswers)