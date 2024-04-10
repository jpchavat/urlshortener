from datetime import datetime

from flask.json.provider import DefaultJSONProvider


class CustomJSONProvider(DefaultJSONProvider):
    """
    Custom JSON provider for Flask that serializes datetime objects to ISO format.
    More info: https://flask.palletsprojects.com/en/3.0.x/api/#flask.json.provider.JSONProvider
    and https://stackoverflow.com/a/74618781/1674908
    """

    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
