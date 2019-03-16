import boto3

class ImageStore:
    def __init__(self,key,secret,region,endpoint):
        self.key=key
        self.secret=secret
        self.region=region
        self.endpoint=endpoint
        self.client=boto3.client('s3', region_name=region, endpoint_url=endpoint,aws_access_key_id=key,aws_secret_access_key=secret)


