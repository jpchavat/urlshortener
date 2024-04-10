from flask import jsonify

from common.exceptions import ItemDoesNotExistException, BadRequestException
from common.logger import logger


def configure_error_handlers(app):
    """
    Configure error handlers for the application.
    """

    @app.errorhandler(ItemDoesNotExistException)
    def handle_item_does_not_exist(error):
        """
        Global error handler for ItemDoesNotExist errors.
        """
        return (
            jsonify(
                {
                    "error_code": error.error_code,
                    "error": "Item does not exist",
                    "params": error.params,
                }
            ),
            404,
        )

    @app.errorhandler(BadRequestException)
    def handle_bad_request(error):
        """
        Global error handler for BadRequest errors.
        """
        return (
            jsonify(
                {
                    "error_code": error.error_code,
                    "error": "Bad request",
                    "params": error.params,
                }
            ),
            400,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """
        Global error handler for unexpected errors.
        """
        raise error
        logger().exception(f"An unexpected error occurred: {error}")
        return (
            jsonify(
                {
                    "error_code": "unexpected_error",
                    "error": "An unexpected error occurred",
                }
            ),
            500,
        )

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error_code": "not_found", "error": "Page not found"}), 404
