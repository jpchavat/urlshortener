from flask import Blueprint, request, jsonify

from common.services.urlobject import URLObjectServices
from common.exceptions import BadRequestException

api = Blueprint("admin", __name__, url_prefix="/admin")


@api.route("/")
def greetings():
    """Returns a greeting message to the user."""
    return "Let's create some short URLs!"


def _get_user_id():
    """
    Returns the user ID of the current user.
    FIXME: This is for PoC purposes only. In a real-world scenario,
        this would be handled by the authentication system.
    """
    # returns admin_{last_4_digits_of_ip}
    return f"admin_{request.remote_addr.replace('.', '')[-6:]}"


@api.route("/urls", methods=["GET"])
def get_short_urls():
    """
    Returns a list of all short URLs created by the admin user.
    Default limit is 50.
    """
    # Get the list of short URLs for the current user
    short_urls = URLObjectServices.get_collection(as_dict=True)
    # short_urls = URLObjectServices.get_short_urls(user_id=_get_user_id(), as_dict=True)  #-> to restricted user access

    # Return the list of short URLs as a JSON response
    return jsonify(short_urls)


def _validate_short_url(short_url):
    """Validates the short URL key, raising an exception if it's invalid."""
    # Short URL key  must be alphanumeric and 6 characters long
    if not short_url.isalnum() or len(short_url) != 6:
        raise BadRequestException(
            error_code="invalid_short_url",
            params={"short_url": short_url},
        )


@api.route("/urls/<short_url>", methods=["GET"])
def get_url_object(short_url):
    """Returns a single URLObject identified by the short URL key."""
    _validate_short_url(short_url)

    # Get the URLObject for the given short URL key
    url_object = URLObjectServices.get_urlobject(short_url, as_dict=True)

    # Return the URLObject as a JSON response
    return jsonify(url_object)


@api.route("/urls", methods=["POST"])
def shorten_url():
    """Given a long URL in the payload, creates a short URL in the system and returns it to the user."""
    # Get the request body as JSON
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "No request body provided"}), 400

    # Extract the long URL from the request body
    long_url = request_data.get("long_url")
    if not long_url:
        return jsonify({"error": "No 'long_url' provided in the request body"}), 400

    # Creates the short URL for the long URL
    short_url = URLObjectServices.create(long_url, user_id=_get_user_id())

    # Return the short URL as a JSON response
    return jsonify({"short_url": short_url}), 201


@api.route("/urls/<short_url>", methods=["DELETE"])
def delete_short_url(short_url):
    """Deletes the URLObject identified by the short URL key."""
    _validate_short_url(short_url)
    # Delete the URLObject for the given short URL key
    URLObjectServices.delete_url(short_url)

    return jsonify({"short_url": short_url})
