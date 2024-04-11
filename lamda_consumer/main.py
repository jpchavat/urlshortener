"""
This scripts simulates the creation of a Lambda function that consumes messages from a
SQS queeue and processes them.
"""

import json
import os
import sys

# add the parent directory to the sys.path
sys.path = [os.path.join(os.path.dirname(__file__), "..")] + sys.path

from common.logger import logger
from common.models.analytic import AnalyticRecord


def lambda_function(message: dict):
    logger().debug(f"Processing message: {message}")

    if message.get("Messages"):
        analytics_data = json.loads(message["Messages"][0]["Body"])
        resp = AnalyticRecord(**analytics_data).save()
        logger().debug(f"Message processed: {resp}")

        # Delete the message from the queue
        receipt_handle = message["Messages"][0]["ReceiptHandle"]
        logger().debug(f"Deleting message: {receipt_handle}")
        response = analytics_srv.client.delete_message(
            QueueUrl=analytics_srv.queue_url,
            ReceiptHandle=receipt_handle,
        )
        logger().debug(f"Message deleted: {response}")


if __name__ == "__main__":
    from admin.app import create_app

    with create_app(load_views=False, load_redis=False, load_db=True).app_context():
        from common.services.sqs import AnalyticsServices

        analytics_srv = AnalyticsServices()

        while True:
            message = analytics_srv.receive(wait_time=20, visibility_timeout=30)
            if message:
                lambda_function(message)
