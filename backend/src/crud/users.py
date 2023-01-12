from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from typing import List

from src.dependencies import oauth2_scheme, SECRET_KEY, ALGORITHM, get_password_hash, verify_password, get_db
from src.schemas.users import User, UserCreate
from src.schemas.tokens import TokenData
from src.db.database import SessionLocal
import src.models as models
import src.schemas as schemas

def authenticate_user(db:Session, username: str, password: str):
    user = get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return False
    return user

def get_all_users(db: Session):
    stmt = select(models.User)
    users = db.scalars(stmt).all()
    return users

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
    return new_user


def remove_user(db: Session, id: int):
    user = get_user(db, id)
    db.delete(user)
    db.commit()
    return {"message": f"User with id={id} was succesfully removed."}

def get_friends(db: Session, user: schemas.User):
    return user.friends

def add_friend(db: Session, user_me_id: int, user_add_id: int):
    user_add = get_user(db, user_add_id)
    user_me = get_user(db, user_me_id)
    if user_add not in user_me.friends and user_me not in user_add.friends:
        user_me.friends.append(user_add)
        user_add.friends.append(user_me)
    elif user_add in user_me.friends and not user_me in user_add.friends:
        user_me.friends.append(user_add)
    elif user_add not in user_me.friends and user_me in user_add.friends:
        user_add.friends.append(user_me)
    else:
        return {"message": f"User with id={user_add_id}  was already your friend."}
    db.commit()
    return {"message": f"User with id={user_add_id} was succesfully added as a friend to account with id={user_me_id}."}

def remove_friend(db: Session, user_me_id: int, user_remove_id: int):
    user_add = get_user(db, user_remove_id)
    user_me = get_user(db, user_me_id)
    if user_add in user_me.friends and user_me in user_add.friends:
        user_me.friends.remove(user_add)
        user_add.friends.remove(user_me)
    elif user_add not in user_me.friends and user_me in user_add.friends:
        user_me.friends.remove(user_add)
    elif user_add in user_me.friends and user_me not in user_add.friends:
        user_add.friends.remove(user_me)
    else:
        return {"message": f"User with id={user_remove_id} was not your friend."}
    db.commit()
    return {"message": f"User with id={user_remove_id} was succesfully removed from friends on account with id={user_me_id}."}
    
    
def get_group(db: Session, id: int):
    stmt = select(models.Group).where(models.Group.id==id)
    group = db.scalar(stmt)
    return group

def get_groups(db: Session):
    stmt = select(models.Group)
    groups = db.scalars(stmt).all()
    return groups

def get_group_by_name(db: Session, name: int):
    stmt = select(models.Group).where(models.Group.name==name)
    group = db.scalar(stmt)
    return group
    
def create_group(db: Session, group: schemas.GroupCreate, creator_id: int):
    creator = get_user(db, creator_id)
    new_group = models.Group(
        name=group.name,
        users=[creator]
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

def remove_group(db: Session, id: int):
    group = get_group(db, id)
    db.delete(group)
    db.commit()
    return {"message": f"Group with id={id} was succesfully removed."}
       
def join_group(db: Session, user_me_id: int, group_id: int):
    user = get_user(db, user_me_id)
    group = get_group(db, group_id)
    if user not in group.users:
        user.groups.append(group)
        return {"message": f"User with id={user_me_id} was added to group with id={group_id}."}
    else:
        return {"message": f"User with id={user_me_id} was already in the group with id={group_id}."}
    
def leave_group(db: Session, user_me_id: int, group_id: int):
    user = get_user(db, user_me_id)
    group = get_group(db, group_id)
    if user in group.users:
        user.groups.remove(group)
        return {"message": f"User with id={user_me_id} was removed from the group with id={group_id}."}
    else:
        return {"message": f"User with id={user_me_id} wasn't member of the group with id={group_id}."}
    
    