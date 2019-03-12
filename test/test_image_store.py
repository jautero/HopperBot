import unittest

class TestImageStore(unittest.TestCase):
    def test_image_store(self):
        from image_store import ImageStore
        dut=ImageStore("foo","bar")
