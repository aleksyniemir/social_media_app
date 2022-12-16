from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from src.dependencies import get_password_hash,  ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_db
from src.crud.users import get_current_user, authenticate_user, get_current_user_if_admin, get_user
from src.schemas.tokens import TokenData
import src.models as models
import src.crud as crud
import src.schemas as schemas

router = APIRouter(
    prefix = "/users",
    tags = ["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    users = crud.get_all_users(db)
    serialized_users = schemas.UserList(users=users)
    return serialized_users

@router.get("/me", status_code=status.HTTP_200_OK)
def get_user_me( db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return current_user
    

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = crud.get_user(db, user_id)
    return user

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_user(
    user: schemas.UserCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_if_admin)
    ) -> models.User:
    user_db_by_username = crud.get_user_by_username(db, username=user.username)
    user_db_by_email = crud.get_user_by_email(db, email=user.email)
    if user_db_by_email or user_db_by_username:
        raise HTTPException(status_code=409, detail="Username or email already exists.")
    new_user = crud.create_user(db, user)
    return new_user


@router.delete("/remove/{id}", tags = ["users"], status_code=status.HTTP_202_ACCEPTED)
def remove_user(id: int, current_user: schemas.User = Depends(get_current_user_if_admin), db: Session = Depends(get_db)): 
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"Person with id={id} does not exist.")   
    mes = crud.remove_user(db, id)
    return mes
    
@router.post("/token", tags = ["users"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): 
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
