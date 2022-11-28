from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta

from src.dependencies import get_password_hash,  ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.crud.users import get_current_user, authenticate_user, get_current_user_if_admin
from src.schemas.roles import Role
from src.schemas.users import User, UserCreate
from src.schemas.tokens import TokenData

router = APIRouter(
    prefix = "/users",
    tags = ["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    #user = next((u for u in fake_users_db if u.id == user_id), None)
    user = next((u for u in fake_users_db if u["id"] == user_id), None)
    return user

@router.get("/me")
def get_users_me(current_user: User = Depends(get_current_user)):
    return current_user
    
@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_user(
    user: UserCreate, current_user: User = Depends(get_current_user_if_admin)
    ) -> User:
    if len(fake_users_db) == 0:
        u_id = 0
    else:
        u_id = max(fake_users_db, key=lambda x: x['id'])['id'] + 1
        #u_id = max(fake_users_db, key=attrgetter('id')).id + 1
        
    hashed_password = get_password_hash(user.password)
    # uncomment when db is configured
    # new_user = models.User(
    #     id=u_id,
    #     username=user.username,
    #     name=user.name,
    #     surname=user.surname,
    #     email=user.email,
    #     role=user.role,
    #     hashed_password=hashed_password
    # )
    user_dict = {
        "id": u_id,
        "username": user.username,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": user.role,
    }
    fake_users_db.append(user_dict)
    return user_dict


@router.delete("/remove/{user_id}", tags = ["users"], status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, current_user: User = Depends(get_current_user_if_admin)):
    global fake_users_db
    #user = next((u for u in fake_users_db if u.id == user_id), None)
    user = next((u for u in fake_users_db if u["id"] == user_id), None)
    
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"Person with id={user_id} does not exist.")   
    
    fake_users_db = [d for d in fake_users_db if d.get("id") != user_id]
    
@router.post("/token", tags = ["users"])
def login(form_data: OAuth2PasswordRequestForm = Depends()): 
    user = authenticate_user(form_data.username, form_data.password)
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
