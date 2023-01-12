from pydantic import BaseModel

class PostBase(BaseModel):
    text: str
    
    class Config:
        orm_mode = True
    
class Post(PostBase):
    id: int
    user_id: int

class PostCreate(PostBase): ...

class PostUpdate(PostBase): ...

class PostDisplay(BaseModel):
    id: int
    text: str
    username: str
    
    class Config:
        orm_mode = True
    
