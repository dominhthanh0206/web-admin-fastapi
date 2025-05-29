from sqlalchemy.orm import Session
from blog.models.user import User
from blog.schemas.user import UserCreate
import uuid

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        db_user = User(
            id=str(uuid.uuid4()),
            username=user.username,
            email=user.email,
            password=user.password,
            full_name=user.full_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: str):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def update_face_embedding(db: Session, user_id: str, face_embedding: bytes):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.face_embedding = face_embedding
        db.commit()
        db.refresh(user)
        return user 