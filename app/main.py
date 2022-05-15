import json
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api.api import api_router
from app.core.config import settings
from app.database.db_session import db_session
from app.models import Circuit, Site

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redocs",
    swagger_ui_init_oauth={
        "useBasicAuthWindowWithAccessCodeGrant": True,
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def hellow_world():
    return {"hello world"}


@app.get("/posts/{id}")
def get_posts(id):
    return {"message": f"posts {id}: this is the posts content"}


@app.delete("/posts/{id}")
def delete_posts(id):
    return {"message": f"posts {id} has been removed"}


@app.post("/posts/")
def post_posts(data: dict):
    return {"message": json.dumps(data)}


@app.get("/dcim/sites/{id}")
def get_dcim_sites(id):
    with db_session() as session:
        result = (
            session.execute(select(Site).where(Site.id == id)).scalars().one_or_none()
        )
        print(result.dict())
        if result is not None:
            return result.dict()
        else:
            return {"message": "sites not found"}


@app.get("/dcim/sites/")
def get_dcim_sites_list(q: Optional[str] = None, limit=10, offset=0):
    with db_session() as session:
        result = (
            session.execute(select(Site).limit(limit).offset(offset)).scalars().all()
        )
        print(result)
        if result is not None:
            sites = [site.dict() for site in result]
            return {"result": sites}
        return {"message": "not found"}


@app.get("/dcim/cricuits/{id}")
def get_dcim_cricuits(id):
    with db_session() as session:
        result = (
            session.execute(select(Circuit).where(Circuit.id == id))
            .scalars()
            .one_or_none()
        )
        print(result, result.dict())
        if result is not None:
            return result.dict()
        else:
            return {"message": "circuit not found"}
