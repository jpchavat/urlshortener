import time
import uuid

from pynamodb.attributes import UnicodeAttribute, NumberAttribute

from common.models.base import BaseModel


class AnalyticRecord(BaseModel):
    class Meta:
        table_name = "analytics"

    id = UnicodeAttribute(hash_key=True, default_for_new=lambda: str(uuid.uuid4()))
    short_url = UnicodeAttribute(range_key=True)
    long_url = UnicodeAttribute()
    ip = UnicodeAttribute(null=True)
    timestamp = NumberAttribute(default_for_new=time.time)
    user_agent = UnicodeAttribute(null=True)
    language = UnicodeAttribute(null=True)
