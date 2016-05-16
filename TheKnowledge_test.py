import unittest
import TheKnowledge

class KnowledgeTestCase(unittest.TestCase):
    def setUp(self):
        self.knowledge=TheKnowledge.TheKnowledge()
        self.knowledge.store("This is a test",("test1","test2"))
    def test_create(self):
        assert self.knowledge != None
    def test_get(self):
        assert self.knowledge.get(("test1","test2"))=="This is a test"