from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from src.dependencies import oauth2_scheme, SECRET_KEY, ALGORITHM, get_password_hash, verify_password 
from src.schemas.roles import Role
from src.schemas.users import User, UserCreate
from src.schemas.tokens import TokenData

fake_users_db = [
    {
        "id": 0,
        "username": "johndoe",
        "name": "john",
        "surname": "Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$LVVUe4vPKiWr/KM3kxYC/urKLcHz.LEx7OvwIHkDjPRpfrURBkLu.",
        "role": Role.user,
    },
    {
        "id": 1,
        "username": "olekniemirka",
        "name": "olek",
        "surname": "niemirka",
        "email": "olekniemirka@example.com",
        "hashed_password": "$2b$12$LVVUe4vPKiWr/KM3kxYC/urKLcHz.LEx7OvwIHkDjPRpfrURBkLu.",
        "role": Role.admin,
    }
]

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return False
    return user

def get_user(username: str):
    user_dict = next((u for u in fake_users_db if u["username"] == username), None)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect user id")
    user = User(**user_dict)
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = get_user(username=token_data.username)
    if not user:
        raise credentials_exception
    return user

def get_current_user_if_admin(user: User = Depends(get_current_user)):
    if user.role == Role.admin:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your role does not have the privelege to remove an user",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
def get_max_id():
    u_id = max(fake_users_db, key=lambda x: x['id'])['id'] + 1
    return u_id
    
def get_user_by_username(username: str):
    user = next((u for u in fake_users_db if u["username"] == username), None)
    return user

def create_user(user: UserCreate):
    u_id = get_max_id()
    hashed_password = get_password_hash(user.password)
    user = {
        "id": u_id,
        "username": user.username,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": user.role,
    }
    fake_users_db.append(user)
    return user