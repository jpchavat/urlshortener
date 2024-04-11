import time
import uuid
from dataclasses import dataclass, asdict
from typing import Optional

from flask import json
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from common.models.base import BaseModel


@dataclass
class AnalyticRecordData:
    id: Optional[str]
    short_url: str
    long_url: str
    ip: str
    timestamp: int
    user_agent: str
    language: str

    def to_json(self):
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(json_data):
        return AnalyticRecordData(**json.loads(json_data))


class AnalyticRecord(BaseModel):
    class Meta:
        table_name = "analytics"

    id = UnicodeAttribute(hash_key=True, default_for_new=uuid.uuid4)
    short_url = UnicodeAttribute(range_key=True)
    long_url = UnicodeAttribute()
    ip = UnicodeAttribute()
    timestamp = NumberAttribute(default_for_new=time.time)
    user_agent = UnicodeAttribute()
    language = UnicodeAttribute()

    @classmethod
    def from_dataclass(cls, data: AnalyticRecordData):
        return cls(
            id=data.id,
            short_url=data.short_url,
            long_url=data.long_url,
            ip=data.ip,
            timestamp=data.timestamp,
            user_agent=data.user_agent,
            language=data.language,
        )

    def to_dataclass(self) -> AnalyticRecordData:
        return AnalyticRecordData(
            id=self.id,
            short_url=self.short_url,
            long_url=self.long_url,
            ip=self.ip,
            timestamp=self.timestamp,
            user_agent=self.user_agent,
            language=self.language,
        )
