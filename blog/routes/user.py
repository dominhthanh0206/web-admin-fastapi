from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from blog.schemas.user import User as UserSchema, UserBase, UserCreate
from blog.models.user import User
from blog.services import user as user_service
from blog.database.database import get_db
from blog.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserSchema)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    )
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )
    return user_service.create_user(db=db, user=user)


@router.get("", response_model=List[UserSchema])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: UserSchema = Depends(get_current_user),
):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: str, db: Session = Depends(get_db), _: UserSchema = Depends(get_current_user)
):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: str,
    user: UserBase,
    db: Session = Depends(get_db),
    _: UserSchema = Depends(get_current_user),
):
    db_user = user_service.update_user(db, user_id=user_id, user_data=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}")
def delete_user(
    user_id: str, db: Session = Depends(get_db), _: UserSchema = Depends(get_current_user)
):
    success = user_service.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
