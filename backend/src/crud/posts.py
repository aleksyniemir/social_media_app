from sqlalchemy.orm import Session
from sqlalchemy.sql import select, update

import src.models as models
import src.crud as crud
import src.schemas as schemas

def create_post(db: Session, post: schemas.PostCreate, user: schemas.User):
    new_post = models.Post(
        text=post.text,
        user_id=user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_post(db: Session, id: int):
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.scalar(stmt)
    return post

def remove_post(db: Session, id: int):
    post = crud.get_post(db, id)
    db.delete(post)
    db.commit()
    return {"message": f"Post with id={id} was succesfully removed."}

def update_post(db: Session, post_update: schemas.PostUpdate,  id: int):
    db.execute(
        update(models.Post)
        .where(models.Post.id == id)
        .values(text=post_update.text)
    )
    db.commit()
    
    return crud.get_post(db, id)

def get_posts(db: Session):
    stmt = select(models.Post)
    posts = db.scalars(stmt).all()
    return posts
    