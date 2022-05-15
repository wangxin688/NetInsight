from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select

from app.api.deps import get_session
from app.core import config, security
from app.models.rbac.users import User  # UserRefreshTokenInput

router = APIRouter()


@router.post("/auth/login")
def login(
    session=Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
):
    result = session.execute(select(User).where(User.email == form_data.username))
    user: User | None = result.scalars().one_or_none()
    if user is None:
        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    if not security.verify_password(form_data.password, user.hash_password):
        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    return user.create_access_token


@router.post("/refresh-token")
def refresh_token(input, session=Depends(get_session)):
    try:
        payload = jwt.decode(
            input.refresh_token,
            config.settings.SECRET_KEY,
            algorithms=[security.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status=status.HTTP_401_BAD_RE, detail=jsonable_encoder(str(e))
        )
    except (jwt.DecodeError, ValidationError) as e:
        raise HTTPException(
            status=status.HTTP_403_FORBIDDEN, detail=jsonable_encoder(str(e))
        )
    token_data = security.TokenPayLoad(**payload)
    if not token_data.refresh:
        raise HTTPException(
            status=status.HTTP_403_FORBIDDEN,
            detail="Could not use access token for refresh",
        )
    now = datetime.utcnow()
    if now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validat credentials, token expires or not valid",
        )
    user = (
        session.execute(select(User).where(User.id == token_data.email))
        .scalars()
        .one_or_none()
    )
    if user is None:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user.create_access_token
