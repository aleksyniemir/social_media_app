from pydantic import BaseModel
from typing import List
from src.schemas.groups import GroupBase

class Role(BaseModel):
    id: int
    role: str
    
    class Config:
        orm_mode = True
    
class UserMinimalInfo(BaseModel):
    id: int
    username: str
    
    class Config:
        orm_mode = True
        
class UserBase(BaseModel):
    username: str
    name: str
    surname: str
    email: str
    friends: List[UserMinimalInfo]
    groups: List[GroupBase]
    
    role: Role

class User(UserBase):
    id: int
    hashed_password: str
    
    class Config:
        orm_mode = True
        
class UserList(BaseModel):
    users: List[User]
    
    class Config:
        orm_mode = True
    
class UserCreate(UserBase): 
    password: str
    

    