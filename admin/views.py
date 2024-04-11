from flask import Blueprint, request, jsonify

from common.exceptions import BadRequestException
from common.services.urlobject import URLObjectServices
from common.validators import validate_short_url

api = Blueprint("admin", __name__, url_prefix="/admin")


@api.before_request
def enforce_json_content_type():
    # FIXME: this can be merged into common.validators
    if request.method in ["POST", "PUT"] and not request.is_json:
        raise BadRequestException(error_code="invalid_content_type")


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


@api.route("/urls/<short_url>", methods=["GET"])
def get_url_object(short_url):
    """Returns a single URLObject identified by the short URL key."""
    validate_short_url(short_url)

    # Get the URLObject for the given short URL key
    url_object = URLObjectServices.get_urlobject(short_url, as_dict=True)

    # Return the URLObject as a JSON response
    return jsonify(url_object)


@api.route("/urls", methods=["POST"])
def shorten_url():
    """Given a long URL in the payload, creates a short URL in the system and returns it to the user."""
    # Get the request body as JSON
    request_data = request.get_json()
    # Extract the long URL from the request body
    long_url = request_data.get("long_url")
    if not long_url:
        raise BadRequestException(error_code="missing_long_url")
    if not long_url.startswith("http") or not long_url.startswith("https"):
        raise BadRequestException(error_code="long_url_not_http_https")

    # Creates the short URL for the long URL
    short_url = URLObjectServices.create(long_url, user_id=_get_user_id(), as_dict=True)

    # Return the short URL as a JSON response
    return jsonify(short_url), 201


@api.route("/urls/<short_url>", methods=["DELETE"])
def delete_short_url(short_url):
    """Deletes the URLObject identified by the short URL key."""
    validate_short_url(short_url)
    # Delete the URLObject for the given short URL key
    URLObjectServices.delete_url(short_url)

    return jsonify({"short_url": short_url})
