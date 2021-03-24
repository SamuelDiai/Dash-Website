from io import BytesIO
from boto3 import client
from botocore.client import Config

import os
import pandas as pd
import yaml

if os.environ.get("AWS_ACCESS_KEY_ID") is None:
    with open("app.yaml", "r") as app_yaml:
        app_file = yaml.safe_load(app_yaml)
    os.environ["AWS_ACCESS_KEY_ID"] = app_file["env_variables"]["AWS_ACCESS_KEY_ID"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = app_file["env_variables"]["AWS_SECRET_ACCESS_KEY"]

AWS_BUCKET_NAME = "age-prediction-site"
CLIENT = client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    config=Config(signature_version="s3v4"),
)


def load_csv(path_in_bucket, **kwargs):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=path_in_bucket)
    df = pd.read_csv(BytesIO(obj["Body"].read()), **kwargs)
    return df


def load_excel(path_in_bucket, **kwargs):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=path_in_bucket)
    df = pd.read_excel(BytesIO(obj["Body"].read()), **kwargs)
    return df