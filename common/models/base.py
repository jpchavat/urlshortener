from common.dynamodb import db


class BaseModel(db.Model):
    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
