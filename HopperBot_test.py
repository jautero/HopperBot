import unittest, json, StringIO
import HopperBot

class MessageUT:
    def __init__(self,msgdict):
        self.__dict__.update(msgdict)

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
        response=self.bot.process(MessageUT({"name":self.nick,"text":"Hello World!"}))
        assert response in self.responses

    def test_pinky(self):
        for question in self.pinkyquestions:
            answer=self.bot.process(MessageUT({"name":self.nick,"text":question.format(self.botname)}))
            assert answer in self.pinkyanswers
    def test_callback(self):
        answer=self.bot.process(MessageUT({"name":self.nick,"text":self.botname +"!"}))
        assert answer == self.nick+"!"
    def test_remembering(self):
        self.bot.remember("Hello World!")
        assert self.bot.memory.get(("hello",))==set(("Hello World!",))
        assert self.bot.memory.get(("world",))==set(("Hello World!",))
    def test_recalling(self):
        self.bot.remember("Hello World!")
        assert self.bot.recall(set(("hello","world")))==set(("Hello World!",))
        self.assertEqual(set(("Hello World!",)), self.bot.recall(set(("hello",))))
        with self.assertRaises(IndexError):
            self.bot.recall(set(("foo","bar")))
    def test_dump(self):
        answer=self.bot.process(MessageUT({"name":self.nick,"text":"dump memory"}))
        dumpstream=StringIO.StringIO()
        self.bot.memory.dump(dumpstream)
        self.assertEqual(dumpstream.getvalue(), answer)
    def test_recalling_message(self):
        msg=MessageUT({"name":self.nick,"text":"Hello World!"})
        self.assert_(self.bot.process(msg) in self.responses)
        self.assertEqual("Hello World!",self.bot.process(msg))

class IDTestCase(unittest.TestCase):
    def setUp(self):
        self.nick="tester"
        self.botname="testbot"
        self.userid="1234"
        self.bot=HopperBot.HopperBot(self.botname)
    def test_id(self):
        self.assertEqual(self.userid,self.bot.process(MessageUT({"name":self.nick,"text":"id?","userid":self.userid})))
