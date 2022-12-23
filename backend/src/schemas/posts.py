from pydantic import BaseModel

class PostBase(BaseModel):
    text: str
    
class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
    
class PostCreate(PostBase): ...

    
