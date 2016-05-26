import unittest, json, StringIO
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
    def test_callback(self):
        answer=self.bot.process(self.nick,self.botname +"!")
        assert answer == self.nick+"!"
    def test_remembering(self):
        self.bot.remember("Hello World!")
        assert self.bot.memory.get(("hello",))==set(("Hello World!",))
        assert self.bot.memory.get(("world",))==set(("Hello World!",))
    def test_recalling(self):
        self.bot.remember("Hello World!")
        assert self.bot.recall(set(("hello","world")))==set(("Hello World!",))
        with self.assertRaises(IndexError):
            self.bot.recall(set(("foo","bar")))
    def test_dump(self):
        answer=self.bot.process(self.nick,"dump memory")
        dumpstream=StringIO.StringIO()
        self.bot.memory.dump(dumpstream)
        self.assertEqual(dumpstream.getvalue(), answer)
