import unittest, json
import HopperBot

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.nick="tester"
        self.botname="testbot"
        self.bot=HopperBot.HopperBot(self.botname)
        pinkydict=json.load(file("pinky.json"))
        self.responses=["I don't see what that has to do with anything!","A likely story!"]
        self.pinkyanswers=[a.format(self.nick) for a in pinkydict["answers"]]
        self.pinkyquestions=pinkydict["questions"]
        
    def test_initialization(self):
        assert self.bot != None

    def test_message_processing(self):
        response=self.bot.process(self.nick,"Hello World!")
        assert response in self.responses
        
    def test_pinky(self):
        for question in self.pinkyquestions:
            answer=self.bot.process(self.nick,question.format(self.botname))
            assert answer in self.pinkyanswers
