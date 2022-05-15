from typing import List, Optional

from sqlalchemy import select

from app.models.dcim.sites import Site, SiteCreate


def get(*, db_session, site_id: int) -> Optional[Site]:
    result = (
        db_session.execute(select(Site).where(Site.id == site_id))
        .scalars()
        .one_or_none()
    )
    return result


def get_all(*, db_session) -> Optional[List[Site]]:
    result = db_session.execute(select(Site)).scalars().all()
    return result


def get_by_code(*, db_session, code: str) -> Optional[Site]:
    result = (
        db_session.execute(select(Site).where(Site.code == code))
        .scalars()
        .one_or_none()
    )
    return result


def get_by_name(*, db_session, name: str) -> Optional[Site]:
    result = (
        db_session.execute(select(Site).where(Site.name == name))
        .scalars()
        .one_or_none()
    )
    return result


def get_all_active(*, db_session) -> Optional[List[Site]]:
    result = (
        db_session.execute(select(Site)).where(Site.status == "Active").scalars().all()
    )
    return result


def create(*, db_session, site_in: SiteCreate) -> Site:
    site = Site(**site_in.dcit())
    db_session.add(site)
    db_session.commit()
