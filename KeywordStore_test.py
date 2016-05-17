import unittest
import KeywordStore

class KeywordStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.kstore=KeywordStore.KeywordStore()
        self.kstore.store("This is a test",("test1","test2"))
    def test_create(self):
        assert self.kstore != None
    def test_get(self):
        assert self.kstore.get(("test1","test2"))==set(("This is a test",))