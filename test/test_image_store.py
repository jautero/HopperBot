import unittest, yaml, os
from image_store import ImageStore

config=yaml.load(open(os.path.expandvars("$WORKSPACE/test/test_config.yaml")), Loader=yaml.SafeLoader)

class TestImageStore(unittest.TestCase):
    def setUp(self):
        self.key=config["store_key"]
        self.secret=config["store_secret"]
        self.region=config["region"]
        self.endpoint=config["endpoint"]
        self.dut=ImageStore(self.key,self.secret,self.region,self.endpoint)

    def test_image_store(self):
        self.assertEqual(self.dut.key,self.key)
        self.assertEqual(self.dut.secret,self.secret)
        self.assertEqual(self.dut.region,self.region)
        self.assertEqual(self.dut.endpoint,self.endpoint)
        
    def test_boto3(self):
        self.assertTrue(self.dut.client)