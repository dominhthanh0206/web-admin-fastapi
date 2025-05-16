from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from blog.schemas.blog import Blog, BlogCreate
from blog.services import blog as blog_service
from blog.database.database import get_db
from blog.services.auth import get_current_user
from blog.models.user import User

router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)

@router.post("", response_model=Blog)
def create_blog(blog: BlogCreate, 
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return blog_service.create_blog(db=db, blog=blog)

@router.get("", response_model=List[Blog])
def read_blogs(skip: int = 0, limit: int = 10, 
              db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    blogs = blog_service.get_blogs(db, skip=skip, limit=limit)
    return blogs

@router.get("/{blog_id}", response_model=Blog)
def read_blog(blog_id: int, 
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    db_blog = blog_service.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog

@router.put("/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, 
               blog: BlogCreate, 
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    db_blog = blog_service.update_blog(db, blog_id=blog_id, blog_data=blog)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog

@router.delete("/{blog_id}")
def delete_blog(blog_id: int, 
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    success = blog_service.delete_blog(db, blog_id=blog_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"detail": "Blog deleted"} 