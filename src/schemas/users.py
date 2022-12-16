from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    username: str
    name: str
    surname: str
    email: str
    #role: Role

class User(UserBase):
    id: int
    hashed_password: str
    
    class Config:
        orm_mode = True
        
class UserList(BaseModel):
    users: List[User]
    
    class Config:
        orm_model = True
    
class UserCreate(UserBase): 
    password: str
    
    