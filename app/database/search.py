from typing import List, Optional

from fastapi.params import Query
from pydantic import Field

from app.models import CircuitRead, HostRead, NetSightBase, SiteRead, UserRead


class SearchBase(NetSightBase):
    query: Optional[str] = Field(None, nullable=True)


class SearchRequest(NetSightBase):
    pass


class ContentResponse(NetSightBase):
    sites = Optional[List[SiteRead]] = Field([], alias="sites")
    hosts = Optional[List[HostRead]] = Field([], alias="hosts")
    circuits = Optional[List[CircuitRead]] = Field([], alias="circuits")
    users = Optional[List[UserRead]] = Field([], alias="users")

    class Config:
        allow_population_by_field_name = True


class SearchResponse(NetSightBase):
    query: Optional[str] = Field(None, nullable=True)
    results: ContentResponse


def search(*, query_str: str, query: Query, model: str, sort=False):
    pass
