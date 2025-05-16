from sqlalchemy.orm import Session
import uuid
from blog.models.user import User
from blog.schemas.user import UserBase, UserCreate
from blog.services.auth import get_password_hash

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        id=str(uuid.uuid4())
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: str, user_data: UserBase):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.username = user_data.username
        db_user.email = user_data.email
        db_user.full_name = user_data.full_name
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False 