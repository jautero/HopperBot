import unittest
from image_store import ImageStore


class TestImageStore(unittest.TestCase):
    def test_image_store(self):
        dut=ImageStore("foo","bar")
