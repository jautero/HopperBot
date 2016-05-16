import unittest
import HopperBot

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.bot=HopperBot.HopperBot()
        self.responses=["I don't see what that has to do with anything!","A likely story!"]
        
    def test_initialization(self):
        assert self.bot != None

    def test_message_processing(self):
        response=self.bot.process("Hello World!")
        assert response in self.responses
        
    def test_pinky(self):
        response=self.bot.process("Are you pondering what I'm pondering?")
        assert response == "Poit, I guess I am."
