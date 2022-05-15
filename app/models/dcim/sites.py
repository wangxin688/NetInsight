import enum
from typing import List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from app.database.db_base import Base
from app.database.models import NameStr, PrimaryKey, TimestampMixin


class SiteStatus(enum.Enum):
    Active = 1
    Planned = 2
    Deployed = 3
    Offline = 4


class SitePriority(enum.Enum):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class SiteClassfication(enum.Enum):
    office = 1
    datacenter = 2
    pop = 3
    remote = 4


class Site(Base, TimestampMixin):
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    status = Column(Enum(SiteStatus), nullable=False)
    priority = Column(Enum(SitePriority))
    classfication = Column(Enum(SiteClassfication), nullable=True)
    asn = Column(String)
    description = Column(String)
    """一对多外键定义规则解释:
    如不在父类中设置passsive_deleles,从代码删除父表数据，字表数据外键会被置空,
    从DB直接删除父表数据,字表数据会被直接删除
    lazy模式为懒加载,默认为select
    使用backref在父级声明,减少声明语句
    在子类中ForienKey()类需要定义ondelete='cascade
    """
    host = relationship("Host", backref="site", lazy="dynamic", passive_deletes=True)
    circuit = relationship(
        "Circuit", backref="site", lazy="dynamic", passive_deletes=True
    )


class SiteBase(BaseModel):
    id: Optional[PrimaryKey]
    code: str
    name: NameStr
    status: SiteStatus
    priority: Optional[str] = Field(None, nullable=True)
    classfication: Optional[str] = Field(None, nullable=True)
    asn: Optional[str] = Field(None, nullable=True)
    description: Optional[str] = Field(None, nullable=True)


class SiteCreate(SiteBase):
    pass


class SiteRead(SiteBase):
    id: Optional[PrimaryKey]
    code: Optional[str]


class SitePagination(BaseModel):
    total: int
    items: List[SiteRead] = []


class SiteUpdate(BaseModel):
    id: Optional[PrimaryKey]
    code: Optional[str] = Field(None, nullable=True)
    name: Optional[NameStr] = Field(None, nullable=True)
    status: Optional[SiteStatus] = Field(None, nullable=True)
    priority: Optional[str] = Field(None, nullable=True)
    classfication: Optional[str] = Field(None, nullable=True)
    asn: Optional[str] = Field(None, nullable=True)
    description: Optional[str] = Field(None, nullable=True)


class SiteDelete(SiteBase):
    id: Optional[PrimaryKey]
    code: Optional[str]
