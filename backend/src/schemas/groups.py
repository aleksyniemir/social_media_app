from pydantic import BaseModel
from typing import List

class GroupBase(BaseModel):
    name: str
    
    class Config:
        orm_mode = True

class GroupCreate(GroupBase): ...

class Group(GroupBase):
    id: int
    
class GroupList(BaseModel):
    groups: List[Group]