import os

import boto3
from flask import current_app

from common.logger import logger
from common.models.analytic import AnalyticRecordData


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
        response = self.get_queue()
        if not response:
            logger().debug(f"Queue not found. Creating a new one.")
            response = self.create_queue()
        self.queue_url = response

    def send(self, analytic_record: AnalyticRecordData) -> dict:
        """Send an Analytic message to the queue."""
        response = self.client.send_message(
            QueueUrl=self.queue_url, MessageBody=analytic_record.to_json()
        )
        logger().debug(f"Message sent: {response}")

        return response

    def receive(self):
        """Receive an Analytic message from the queue."""
        response = self.client.receive_message(
            QueueUrl=self.queue_url, MaxNumberOfMessages=1
        )
        logger().debug(f"Message received: {response}")
        if "Messages" in response:
            return AnalyticRecordData.from_json(response["Messages"][0]["Body"])
        return None

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
