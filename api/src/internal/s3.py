import boto3
import os
from botocore.client import Config

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.environ.get("MINIO_ENDPOINT"),
        aws_access_key_id=os.environ.get("MINIO_ROOT_USER"),
        aws_secret_access_key=os.environ.get("MINIO_ROOT_PASSWORD"),
        config=Config(signature_version='s3v4'),
        region_name="us-east-1",
    )