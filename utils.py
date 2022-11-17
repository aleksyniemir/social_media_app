from schemas import User, Role, TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import List, Dict
from schemas import User, UserInDB
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "41cf6049116ed36440bd2fc311485f89d3a485bf05e97a3ac03412566abb21f0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

def fake_decode_token(token):
    return User(
        id = 0,
        username = "dupaaa",
        name = token,
        surname = "str",
        email = "ee",
        hashed_password = "ddd",
        role = Role.user
    )

def get_user(username: str):
    user_dict = next((u for u in fake_users_db if u["username"] == username), None)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect user id")
    user = UserInDB(**user_dict)
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

def get_current_user_if_admin(user: schemas.User = Depends(get_current_user)):
    if user.role == Role.admin:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your role does not have the privelege to remove an user",
            headers={"WWW-Authenticate": "Bearer"},
        )
        

def hash_password(plain_password: str):
    return plain_password + "_fakehash"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return False
    return user

def get_max_id():
    u_id = max(fake_users_db, key=lambda x: x['id'])['id'] + 1
    return u_id
    
def get_user_by_username(username: str):
    user = next((u for u in fake_users_db if u["username"] == username), None)
    return user

def create_user(user: schemas.UserIn):
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
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt