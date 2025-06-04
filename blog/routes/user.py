import json
from fastapi import APIRouter, Depends, Form, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from blog.schemas.user import User as UserSchema, UserBase, UserCreate, FaceRecognitionResponse
from blog.models.user import User
from blog.services import user as user_service
from blog.database.database import get_db
from blog.services.auth import get_current_user, get_user_by_id
from blog.services.user_service import UserService
from blog.services.face_recognition_service import FaceRecognitionService

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
async def update_user(
    user_id: str,
    username: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    _: UserSchema = Depends(get_current_user),
):
    user_data = get_user_by_id(db, user_id)
    if user_data is None:
        raise HTTPException(status_code=400, detail="User not found")

    user_base = UserBase(
        username=username if username is not None else user_data.username,
        email=email if email is not None else user_data.email,
        full_name=full_name if full_name is not None else user_data.full_name,
    )

    face_embedding = None
    if file:
        image_data = await file.read()
        face_embedding = FaceRecognitionService.get_face_embedding(image_data)
        if face_embedding is None:
            raise HTTPException(status_code=400, detail="Không tìm thấy khuôn mặt trong ảnh")
        face_embedding = FaceRecognitionService.encode_embedding(face_embedding)

    db_user = user_service.update_user(
        db, user_id=user_id, user_data=user_base, face_embedding=face_embedding
    )
    return db_user


@router.delete("/{user_id}")
def delete_user(
    user_id: str, db: Session = Depends(get_db), _: UserSchema = Depends(get_current_user)
):
    success = user_service.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


@router.post("/recognize-face/", response_model=FaceRecognitionResponse)
async def recognize_face(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_data = await file.read()
    
    face_embedding = FaceRecognitionService.get_face_embedding(image_data)
    if face_embedding is None:
        return FaceRecognitionResponse(message="Không tìm thấy khuôn mặt trong ảnh")
    
    users = UserService.get_all_users(db)
    for user in users:
        if user.face_embedding and FaceRecognitionService.compare_faces(user.face_embedding, face_embedding):
            return FaceRecognitionResponse(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                message="Đã nhận diện thành công"
            )
    
    return FaceRecognitionResponse(message="Không xác định")
