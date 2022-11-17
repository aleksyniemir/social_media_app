from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    password: str
    role: Role
    
    class Config:
        orm_mode = True
    
class Post(BaseModel):
    id: int
    user_id: int
    text: str
    