from flask.logging import create_logger
from flask import current_app


def logger():
    return create_logger(current_app)
