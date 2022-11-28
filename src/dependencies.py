from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from db.database import SessionLocal, engine

import src.schemas as schemas
from src.schemas.roles import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
SECRET_KEY = "41cf6049116ed36440bd2fc311485f89d3a485bf05e97a3ac03412566abb21f0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def fake_decode_token(token):
    return schemas.User(
        id = 0,
        username = "dupaaa",
        name = token,
        surname = "str",
        email = "ee",
        hashed_password = "ddd",
        role = Role.user
    )

def hash_password(plain_password: str):
    return plain_password + "_fakehash"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()