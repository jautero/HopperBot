import unittest, yaml, os
from image_store import ImageStore

config=yaml.load(open(os.path.expandvars("$WORKSPACE/test/test_config.yaml")))

class TestImageStore(unittest.TestCase):
    def setUp(self):
        self.key=config["store_key"]
        self.secret=config["store_secret"]
    def test_image_store(self):
        dut=ImageStore(self.key,self.secret)
        self.assertEqual(dut.key,self.key)
        self.assertEqual(dut.secret,self.secret)
