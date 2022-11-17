from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    username: str
    name: str
    surname: str
    email: str
    role: Role
    
    class Config:
        orm_mode = True

class UserInDB(User):
    id: int
    hashed_password: str
    
class UserIn(User): 
    password: str
    
class Post(BaseModel):
    id: int
    user_id: int
    text: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None

    
    