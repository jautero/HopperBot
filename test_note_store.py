import unittest
from note_store import NoteStore, DictNoteStore

class TestBaseClass(unittest.TestCase):
    def setUp(self):
        self.store=NoteStore()
        self.note={'name':'foo'}


    def test_find(self):
        with self.assertRaises(NotImplementedError):
            self.store.find(self.note['name'])

    def test_store(self):
        with self.assertRaises(NotImplementedError):
            self.store.store(self.note)

    def test_unique_note(self):
        with self.assertRaises(NotImplementedError):
            self.store.unique_name()

class TestDictStore(unittest.TestCase):
    def setUp(self):
        self.store=DictNoteStore()
        self.note={'name':'foo'}

    def test_find_not_existing_note(self):
        self.assertEqual(None,self.store.find("foobar"))

    def test_find_existing_note(self):
        self.store.store(self.note)
        self.assertEqual(self.note,self.store.find(self.note['name']))

    def test_unique_note(self):
        name1=self.store.unique_name()
        note={'name':name1}
        self.store.store(note)
        name2=self.store.unique_name()
        self.assertNotEqual(name1,name2)
