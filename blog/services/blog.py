from sqlalchemy.orm import Session
from blog.models.blog import Blog
from blog.schemas.blog import BlogCreate

def create_blog(db: Session, blog: BlogCreate):
    db_blog = Blog(title=blog.title, content=blog.content)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Blog).offset(skip).limit(limit).all()

def get_blog(db: Session, blog_id: int):
    return db.query(Blog).filter(Blog.id == blog_id).first()

def update_blog(db: Session, blog_id: int, blog_data: BlogCreate):
    db_blog = get_blog(db, blog_id)
    if db_blog:
        db_blog.title = blog_data.title
        db_blog.content = blog_data.content
        db.commit()
        db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    db_blog = get_blog(db, blog_id)
    if db_blog:
        db.delete(db_blog)
        db.commit()
        return True
    return False 