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
    def test_nonexistent_keyword(self):
        assert not self.kstore.get(("test3",))
    def test_one_keyword(self):
        self.kstore.store("This is another test",("test1",))
        assert self.kstore.get(("test1",))==set(("This is another test","This is a test"))