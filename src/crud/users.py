from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.dependencies import oauth2_scheme, SECRET_KEY, ALGORITHM, get_password_hash, verify_password, get_db
from src.schemas.users import User, UserCreate
from src.schemas.tokens import TokenData
from src.db.database import SessionLocal
import src.models as models

def authenticate_user(db:Session, username: str, password: str):
    user = get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return False
    return user

def get_user(db: Session, id: int):
    stmt = select(models.User).where(models.User.id == id)
    user = db.scalar(stmt)
    return user

def get_user_by_username(db: Session, username: str):
    stmt = select(models.User).where(models.User.username == username)
    user = db.scalar(stmt)
    return user

def get_user_by_email(db: Session, email: str):
    stmt = select(models.User).where(models.User.email == email)
    user = db.scalar(stmt)
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, token_data.username)
    if not user:
        raise credentials_exception
    return user

def get_current_user_if_admin(user: User = Depends(get_current_user)):
    # if user.role == Role.admin:
    #     return user
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Your role does not have the privelege to remove an user",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    return 1

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        name=user.name,
        surname=user.surname,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user

def get_all_users(db: Session):
    stmt = select(models.User)
    users = db.scalars(stmt).all()
    return users

def remove_user(db: Session, id: int):
    user = get_user(db, id)
    db.delete(user)
    db.commit()
    return {"message": "User was succesfully removed."}