import enum
from typing import List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.types import Enum

from app.database.db_base import Base
from app.database.models import NameStr, PrimaryKey, TimestampMixin
from app.models.dcim.sites import Site


class CircuitStatus(enum.Enum):
    Active = 1
    Planned = 2
    Deployed = 3
    Offline = 4


class Circuit(Base, TimestampMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    local_ip = Column(String, index=True)
    gateway = Column(String, index=True)
    status = Column(Enum(CircuitStatus))
    terminal_a = Column(String, nullable=False, unique=True)
    terminal_z = Column(String, nullable=False, unique=True)
    site_id = Column(Integer, ForeignKey(Site.id, ondelete="cascade"))


class CircuitBase(BaseModel):
    id: Optional[PrimaryKey]
    name: NameStr
    local_ip: Optional[str]
    gateway: Optional[str]
    status: CircuitStatus
    terminal_a: Optional[str]
    terminal_z: Optional[str]


class CircuitCreate(CircuitBase):
    pass


class CircuitRead(CircuitBase):
    id: Optional[PrimaryKey]
    code: Optional[str]


class CircuitPagination(BaseModel):
    total: int
    items: List[CircuitRead] = []


class HostUpdate(BaseModel):
    id: Optional[PrimaryKey]
    hostname: Optional[NameStr] = Field(None, nullable=True)
    status: Optional[CircuitStatus] = Field(None, nullable=True)
    management_ip: Optional[str] = Field(None, nullable=True)
    serial: Optional[str] = Field(None, nullable=True)


class CircuitDelete(CircuitBase):
    id: Optional[PrimaryKey]
