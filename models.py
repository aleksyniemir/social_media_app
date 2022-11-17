from database import Base
from classes import Role
from sqlalchemy import String, Integer, Enum, Column

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable = False)
    surname = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False)
    password = Column(String(255))
    role = Column(Enum(Role))
    