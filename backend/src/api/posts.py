from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from src.dependencies import get_password_hash,  ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_db
from src.crud.users import *
from src.crud.posts import create_post
from src.schemas.tokens import Token
import src.models as models
import src.crud as crud
import src.schemas as schemas

router = APIRouter(
    prefix = "/posts",
    tags = ["posts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_post(
    post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)
) -> models.Post:
    new_post = crud.create_post(db, post, current_user)
    return new_post

@router.delete("/remove", status_code=status.HTTP_201_CREATED)
def remove_post(
    id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)
) -> models.Post:
    post = crud.get_post(db, id)
    if post.user_id != current_user.id and current_user.role.role != "admin":
        return {"message": f"User doesn't have priveleges to delete post with id={id}"}   
    msg = crud.remove_post(db, id)
    return msg
    
@router.put("/update", status_code=status.HTTP_200_OK)
def update_post(
    post_update: schemas.PostUpdate, id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)
) -> models.Post:
    post = crud.get_post(db, id)
    if post.user_id != current_user.id and current_user.role.role != "admin":
        return {"message": f"User doesn't have priveleges to delete post with id={id}"}   
    updated_post = crud.update_post(db, post_update,  id)
    return updated_post

@router.get("/", status_code=status.HTTP_200_OK)
def get_posts(n_page: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user), username_filter: str | None = None):
    
    posts = crud.get_posts(db)
    posts_to_display = []
    if username_filter == None or username_filter == "undefined":
        for post in posts:
            username = crud.get_user(db, post.user_id).username
            posts_to_display.append(schemas.PostDisplay(
                text=post.text,
                username=username,
                id=post.id
            ))
    else:
        for post in posts:
            username = crud.get_user(db, post.user_id).username
            if username_filter == username:
                posts_to_display.append(schemas.PostDisplay(
                    text=post.text,
                    username=username,
                    id=post.id
                ))
        
    posts_to_display = posts_to_display[
        (n_page - 1) * 5 : (n_page - 1) * 5 + 5]
    return posts_to_display

@router.get("/number_of_pages", status_code=status.HTTP_200_OK)
def get_number_of_pages(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    posts = crud.get_posts(db)
    n_of_pages = int(len(posts)/5) + 1
    return n_of_pages