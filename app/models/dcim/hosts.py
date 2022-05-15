import enum
from typing import List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.types import Enum

from app.database.db_base import Base
from app.database.models import NameStr, PrimaryKey, TimestampMixin
from app.models.dcim.sites import Site


class HostStatus(enum.Enum):
    Active = 1
    Planned = 2
    Deployed = 3
    Offline = 4


class Host(Base, TimestampMixin):
    id = Column(Integer, primary_key=True)
    hostname = Column(String, nullable=False, index=True)
    management_ip = Column(String, index=True)
    serial = Column(String, nullable=False, unique=True)
    status = Column(Enum(HostStatus))
    site_id = Column(Integer, ForeignKey(Site.id, ondelete="cascade"))


class HostBase(BaseModel):
    id: Optional[PrimaryKey]
    hostname: NameStr
    management_ip: str
    status: HostStatus
    serial: Optional[str] = Field(None, nullable=True)


class HostCreate(HostBase):
    pass


class HostRead(HostBase):
    id: Optional[PrimaryKey]
    code: Optional[str]


class HostPagination(BaseModel):
    total: int
    items: List[HostRead] = []


class HostUpdate(BaseModel):
    id: Optional[PrimaryKey]
    hostname: Optional[NameStr] = Field(None, nullable=True)
    status: Optional[HostStatus] = Field(None, nullable=True)
    management_ip: Optional[str] = Field(None, nullable=True)
    serial: Optional[str] = Field(None, nullable=True)


class HostDelete(HostBase):
    id: Optional[PrimaryKey]
