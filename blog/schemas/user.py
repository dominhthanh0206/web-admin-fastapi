from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    id: str | None = None


class FaceRecognitionResponse(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    message: str 