from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select

from app.api.deps import get_current_user, get_session
from app.core.security import get_password_hash
from app.models.rbac.users import (User, UserRead, UserRegister,
                                   UserRegisterResponse, UserUpdate)

router = APIRouter()


@router.get("/me", response_model=UserRead)
# @router.get("/me")
def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete("/me", status_code=204)
def delete_user(
    current_user: User = Depends(get_current_user), session=Depends(get_session)
):
    session.execute(delete(User).where(User.id == current_user.id))
    session.commit()


@router.post("/reset-password")
async def reset_current_user_password(
    user_update_password: UserUpdate,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Update current user password"""
    current_user.hashed_password = get_password_hash(user_update_password.password)
    session.add(current_user)
    await session.commit()
    return current_user


@router.post("/register", response_model=UserRegisterResponse)
async def register_new_user(
    new_user: UserRegister,
    session=Depends(get_session),
):
    """Create new user"""
    result = session.execute(select(User).where(User.email == new_user.email))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Cannot use this email address")
    user = User(
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
    )
    session.add(user)
    session.commit()
    return user
