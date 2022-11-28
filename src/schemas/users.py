from pydantic import BaseModel
from src.schemas.roles import Role

class UserBase(BaseModel):
    username: str
    name: str
    surname: str
    email: str
    role: Role

class User(UserBase):
    id: int
    hashed_password: str
    
    class Config:
        orm_mode = True
    
class UserCreate(UserBase): 
    password: str
    
    