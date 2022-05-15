from datetime import datetime, timedelta
from typing import List, Optional

from jose import jwt
from pydantic import BaseModel, Field, validator
from pydantic.networks import EmailStr
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.types import Enum

from app.core.config import settings
from app.core.security import get_password_hash
from app.database.db_base import Base
from app.database.models import PrimaryKey, TimestampMixin
from app.models.rbac.groups import Group, GroupRead
from app.utils.enums import UserRoles

# from sqlalchemy_utils import TSVectorType


class User(Base, TimestampMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRoles), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    group_id = Column(Integer, ForeignKey(Group.id))
    # search_vector = Column(TSVectorType("email", weight={"email": "A"}))

    @property
    def create_access_token(self):
        now = datetime.utcnow()
        expires_at = now + timedelta(minutes=settings.JWT_TOKEN_EXPIRE)
        data1 = {"expires_at": expires_at, "email": self.email, "refresh": False}
        data2 = {"expires_at": expires_at, "email": self.email, "refresh": True}
        access_token, expires_at = jwt.encode(
            data1, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        refresh_token, refresh_token_expires_at = jwt.encode(
            data2, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return {
            "code": 0,
            "data": {
                "token": {
                    "token_type": "Bearer",
                    "access_token": access_token,
                    "expires_at": expires_at,
                    "refresh_token": refresh_token,
                    "refresh_token_expires_at": refresh_token_expires_at,
                },
                "user": {
                    "email": self.email,
                    "role": self.role,
                    "is_active": self.is_active,
                },
            },
            "msg": "success",
        }


class UserGroup(BaseModel):
    group: GroupRead


class UserBase(BaseModel):
    email: EmailStr
    role: str
    is_active: str

    @validator("email")
    def email_required(cls, value):
        if not value:
            raise ValueError("Must not be empty string and must be a email")
        return value


class UserLogin(UserBase):
    password: str

    @validator("password")
    def password_required(cls, value):
        if not value:
            raise ValueError("Must not be empty string")
        return value


class UserRegister(UserLogin):
    password: str

    @validator("password", pre=True, always=True)
    def password_required(cls, value):
        password = value
        return get_password_hash(password)


class UserLoginResponse(BaseModel):
    token_type: str
    access_token: str
    expires_at: str
    refresh_token: str
    refresh_token_expires_at: str


class UserRead(UserBase):
    id: PrimaryKey
    role: Optional[str] = Field(None, nullable=True)


class UserUpdate(BaseModel):
    id: PrimaryKey
    password: Optional[str] = Field(None, nullable=True)
    role: Optional[str] = Field(None, nullable=True)
    group: Optional[str] = Field(None, nullable=True)

    @validator("password", pre=True)
    def hash(cls, value):
        return get_password_hash(str(value))


class UserRegisterResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: str


class UserPagination(BaseModel):
    total: int
    items: List[UserRead] = []


class UserRefreshTokenInput(BaseModel):
    refresh_token: str
