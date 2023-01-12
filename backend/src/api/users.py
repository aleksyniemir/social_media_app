from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from src.dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_db
from src.crud.users import get_current_user, authenticate_user 
from src.schemas.tokens import Token
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
def get_user_me(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return current_user
    

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = crud.get_user(db, id)
    return user

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_user(
    user: schemas.UserCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)
    ) -> models.User:
    user_db_by_username = crud.get_user_by_username(db, username=user.username)
    user_db_by_email = crud.get_user_by_email(db, email=user.email)
    if user_db_by_email or user_db_by_username:
        raise HTTPException(status_code=409, detail="Username or email already exists.")
    new_user = crud.create_user(db, user)
    return new_user


@router.delete("/remove/{id}", status_code=status.HTTP_202_ACCEPTED)
def remove_user(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)): 
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"Person with id={id} does not exist.")   
    msg = crud.remove_user(db, id)
    return msg

@router.get("/me/friends", status_code=status.HTTP_200_OK)
def get_friends(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    friends = crud.get_friends(db, current_user)
    return friends

@router.put("/add_friend/{id}", status_code=status.HTTP_200_OK)
def add_friend(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    msg = crud.add_friend(db, user_me_id=current_user.id, user_add_id=id)
    return msg
    
@router.delete("/remove_friend/{id}", status_code=status.HTTP_200_OK)
def remove_friend(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    msg = crud.remove_friend(db, user_me_id=current_user.id, user_remove_id=id)
    return msg

@router.get("/group/{id}", status_code=status.HTTP_200_OK)
def get_group(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    group = crud.get_group(db, id)
    if not group:
        return {"message": f"Group with id={id} does not exist."}
    return group

@router.get("/me/groups", status_code=status.HTTP_200_OK)
def get_users_groups(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return current_user.groups

@router.get("/groups", status_code=status.HTTP_200_OK)
def get_groups(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    groups = crud.get_groups(db)
    return groups

@router.put("/join_group/{id}", status_code=status.HTTP_200_OK)
def join_group(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    msg = crud.join_group(db, user_me_id=current_user.id, group_id=id)
    return msg

@router.delete("/leave_group/{id}", status_code=status.HTTP_200_OK)
def leave_group(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    msg = crud.leave_group(db, user_me_id=current_user.id, group_id=id)
    return msg

@router.post("/create_group")
def create_group(group: schemas.GroupCreate, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    group_in_db = crud.get_group_by_name(db, group.name)
    if group_in_db:
        raise HTTPException(status_code=409, detail="Group with such name already exists.")
    new_group = crud.create_group(db, group, creator_id=current_user.id)
    return new_group

@router.delete("/remove_group/{id}", status_code=status.HTTP_202_ACCEPTED)
def remove_group(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)): 
    group = crud.get_group(db, id)
    if not group:
        raise HTTPException(
            status_code=404, 
            detail=f"Group with id={id} does not exist.")   
    msg = crud.remove_group(db, id)
    return msg
    
@router.post("/token", tags = ["users"], response_model=Token)
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
    print("access_token: " + access_token + ", token_type: " +  "bearer")
    return {"access_token": access_token, "token_type": "bearer"}

