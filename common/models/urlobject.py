from dataclasses import dataclass
from datetime import datetime, timezone

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
from common.models.base import BaseModel


@dataclass
class URLObject(BaseModel):
    class Meta:
        table_name = "urls"

    # The short_url is the hash key for the table, MUST be unique always
    short_url = UnicodeAttribute(hash_key=True)
    long_url = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(
        default_for_new=lambda: datetime.now(timezone.utc)
    )
    user_id = UnicodeAttribute()
    deleted = BooleanAttribute(default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<URLObject {self.short_url} {self.long_url}>"
