from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from src.db.database import Base

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    role = Column(String(255), nullable = False, unique = True)
    users = relationship("User", backref="role")