from flask import Blueprint, request, redirect

from common.exceptions import BadRequestException
from common.services.urlobject import URLObjectServices
from common.validators import validate_short_url

api = Blueprint("api", __name__)


@api.before_request
def enforce_json_content_type():
    """Enforce that all POST and PUT requests are JSON."""
    # FIXME: this can be merged into common.validators
    if request.method in ["POST", "PUT"] and not request.is_json:
        raise BadRequestException(error_code="invalid_content_type")


@api.route("/<short_url>")
def redirect_short_url(short_url: str):
    # validate the short URL key (must be an alphanum of 6 characters)
    validate_short_url(short_url)
    # Prepare the analytics data
    analytics = {
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "language": request.headers.get("Accept-Language"),
    }
    long_url = URLObjectServices.process_redirection(short_url, analytics=analytics)
    return redirect(long_url, code=302)
