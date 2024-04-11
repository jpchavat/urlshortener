import os
from dotenv import load_dotenv

load_dotenv(
    # Path to the .env file in the same directory as this file
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    verbose=True,
)


class Config(object):
    AWS_SQS_ENDPOINT = os.environ.get("AWS_SQS_ENDPOINT")
    AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    DYNAMODB_HOST = os.environ.get("AWS_DYNAMODB_HOST")
    DYNAMODB_AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
    DYNAMODB_AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
    DYNAMODB_READ_CAPACITY_UNITS = 1  # ignored when using DynamoDB in on-demand mode -> https://github.com/pynamodb/PynamoDB/issues/629#issuecomment-517898130
    DYNAMODB_WRITE_CAPACITY_UNITS = 1  # ignored when using DynamoDB in on-demand mode
    REDIS_URL = os.environ.get("REDIS_URL")
