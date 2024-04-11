import json

import boto3
from flask import current_app

from common.logger import logger


class AnalyticsServices:
    """Wrapper for the SQS service to send/receive analytic messages."""

    QUEUE_NAME = "analytics"

    def __init__(self):
        # client depends on the setting values
        self.client = boto3.client(
            "sqs",
            endpoint_url=current_app.config["AWS_SQS_ENDPOINT"],
            region_name=current_app.config["AWS_DEFAULT_REGION"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
        )

        # Assure the queue exists
        try:
            response = self.get_queue()
            if not response:
                logger().debug(f"Queue not found. Creating a new one.")
                response = self.create_queue()
        except Exception as e:
            # FIXME: double check (empty response plus exception) due to
            #  strange behavior of the get_queue method
            #  It needs to be researched and fixed (mind the version of boto3 and botocore)
            logger().debug(f"Queue not found. Creating a new one.")
            response = self.create_queue()
        self.queue_url = response

    def send(self, analytic_record: dict) -> dict:
        """Send an Analytic message to the queue."""
        response = self.client.send_message(
            QueueUrl=self.queue_url, MessageBody=json.dumps(analytic_record)
        )
        logger().debug(f"Message sent: {response}")

        return response

    def receive(self, wait_time: int = 20, visibility_timeout: int = 30) -> dict:
        """Receive an Analytic message from the queue."""
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=wait_time,
            VisibilityTimeout=visibility_timeout,
        )
        logger().debug(f"Message received: {response}")
        return response

    def create_queue(self):
        """Create the Analytics standard queue with the given name."""
        response = self.client.create_queue(
            QueueName=self.QUEUE_NAME,
            Attributes={
                "DelaySeconds": "0",
                "MessageRetentionPeriod": "86400",  # 1 day, will be ok for the PoC
            },
        )
        logger().debug(f"Queue created: {response}")
        return response.get("QueueUrl")

    def delete_queue(self, queue_url: str):
        """Delete the queue with the given URL."""
        logger().debug(f"Deleting queue: {queue_url}")
        self.client.delete_queue(QueueUrl=queue_url)

    def get_queue(self) -> dict:
        """Get the Analytics queue from the SQS service, if it exists."""
        response = self.client.get_queue_url(QueueName=self.QUEUE_NAME)
        return response["QueueUrls"] if "QueueUrls" in response else []
