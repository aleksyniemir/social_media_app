from sqlalchemy import String, Integer, Enum, Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.models.users import User

from src.models.users import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    text = Column(String(4000), nullable=True)

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship("User", back_populates="posts")