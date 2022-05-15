from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select

from app.core.config import settings
from app.core.security import TokenPayLoad
from app.database.db_session import db_session
from app.models.rbac.users import User

oauth2_token = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_session():
    with db_session() as session:
        yield session


def get_current_user(session=Depends(get_session), token=Depends(oauth2_token)) -> User:
    try:
        payload = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=[settings.SECRET_ALGORITHM]
        )
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    token_data = TokenPayLoad(**payload)

    result = session.execute(select(User).where(User.email == token_data.email))
    user: User | None = result.scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

class RoleChecker