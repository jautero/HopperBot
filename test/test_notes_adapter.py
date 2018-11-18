import unittest
import notes_adapter

class TestRemoveStart(unittest.TestCase):
    def test_remove_empty(self):
        self.assertEqual("foo",notes_adapter.remove_start("foo",""))
    def test_empty_original(self):
        self.assertEqual("",notes_adapter.remove_start("","foo"))
        self.assertEqual("",notes_adapter.remove_start("",""))
    def test_happy_day(self):
        self.assertEqual("bar",notes_adapter.remove_start("foobar","foo"))
    def test_no_remove_end(self):
        self.assertEqual("barfoo",notes_adapter.remove_start("barfoo","foo"))
