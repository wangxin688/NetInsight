from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if settings.ENVIRONMENT == "DEV":
    sqlalchemy_database_uri = settings.DEFAULT_SQLITE_URL
else:
    sqlalchemy_database_uri = settings.DEFAULT_SQLALCHEMY_DATABASE_URI

engine = create_engine(sqlalchemy_database_uri, pool_pre_ping=True)


db_session = sessionmaker(bind=engine, expire_on_commit=False)
