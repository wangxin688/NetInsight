from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_TOKEN_EXPIRE = settings.JWT_TOKEN_EXPIRE
JWT_TOKEN_REFRESH = settings.JWT_TOKEN_REFRESH
SECRET_KEY = settings.SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str):
    return pwd_context.verify(plain_password, hash_password)


class TokenPayLoad(BaseModel):
    sub: str
    refresh: bool
    exp: int
