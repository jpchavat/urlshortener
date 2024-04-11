from common.exceptions import BadRequestException


def validate_short_url(short_url):
    """Validates the short URL key, raising an exception if it's invalid."""
    # Short URL key  must be alphanumeric and 6 characters long
    if not short_url.isalnum() or len(short_url) != 6:
        raise BadRequestException(
            error_code="invalid_short_url",
            params={"short_url": short_url},
        )
