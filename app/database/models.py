from datetime import datetime

from pydantic import BaseModel
from pydantic.types import SecretStr, conint, constr
from sqlalchemy import Column, DateTime, event

NameStr = constr(regex=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)
PrimaryKey = conint(gt=0, lt=2147483647)


class NetInsight(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

    json_encoders = {
        datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
        SecretStr: lambda v: v.get_secret_value() if v else None,
    }


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def _update_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last(cls):
        # hooks for MapperEvents.after_configured()
        event.listen(cls, "before_update", cls._update_at)
