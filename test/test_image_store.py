import unittest
from image_store import ImageStore


class TestImageStore(unittest.TestCase):
    def setUp(self):
        self.secret="bar"
        self.key="foo"
    def test_image_store(self):
        dut=ImageStore(self.key,self.secret)
        self.assertEqual(dut.key,self.key)
        self.assertEqual(dut.secret,self.secret)
