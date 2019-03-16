import unittest, yaml, os
from image_store import ImageStore

config=yaml.load(open(os.path.expandvars("$WORKSPACE/test/test_config.yaml")), Loader=yaml.SafeLoader)

class TestImageStore(unittest.TestCase):
    def setUp(self):
        self.key=config["store_key"]
        self.secret=config["store_secret"]
        self.region=config["region"]
        self.endpoint=config["endpoint"]
    def test_image_store(self):
        dut=ImageStore(self.key,self.secret,self.region,self.endpoint)
        self.assertEqual(dut.key,self.key)
        self.assertEqual(dut.secret,self.secret)
        self.assertEqual(dut.region,self.region)
        self.assertEqual(dut.endpoint,self.endpoint)
        
    def test_boto3(self):
        dut=ImageStore(self.key,self.secret,self.region,self.endpoint)
        self.assertTrue(dut.client)