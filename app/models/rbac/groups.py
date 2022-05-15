from typing import List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship

from app.database.db_base import Base
from app.database.models import NameStr, PrimaryKey, TimestampMixin
from app.utils.slugify import slugify


class Group(Base, TimestampMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    slug = Column(String)
    description = Column(String)
    default = Column(Boolean)
    user = relationship("User", backref="group", lazy="dynamic", passive_deletes=True)


def generate_slug(target, value, oldvalue, initiator):
    if value and (not target.slug or value != oldvalue):
        target.slug = slugify(value, seperator="_")


listen(Group.name, "set", generate_slug)


class GroupBase(BaseModel):
    id: Optional[PrimaryKey]
    name: NameStr
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(None, nullable=True)


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: Optional[PrimaryKey]
    slug: Optional[str]


class GroupUpdate(BaseModel):
    id: Optional[PrimaryKey]
    name: NameStr
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(None, nullable=True)


class GroupPagination(BaseModel):
    total: int
    items: List[GroupRead] = []
