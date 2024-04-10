import os


class Config:
    AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")
    DYNAMODB_HOST = os.environ.get("AWS_DYNAMODB_HOST")
    DYNAMODB_AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    DYNAMODB_AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    DYNAMODB_READ_CAPACITY_UNITS = 1  # ignored when using DynamoDB in on-demand mode -> https://github.com/pynamodb/PynamoDB/issues/629#issuecomment-517898130
    DYNAMODB_WRITE_CAPACITY_UNITS = 1  # ignored when using DynamoDB in on-demand mode
