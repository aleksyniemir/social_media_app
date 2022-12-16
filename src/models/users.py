from sqlalchemy import String, Integer, Enum, Column, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    role = Column(String(255), nullable = False, unique = True)
    users = relationship("User", backref="role")
    

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable = False, unique=True)
    name = Column(String(255), nullable = False)
    surname = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False, unique=True)
    hashed_password = Column(String(255))

    role_id = Column(Integer, ForeignKey(Role.id), nullable = False)
    



     