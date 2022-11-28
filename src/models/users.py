from src.db.database import Base
from src.schemas.roles import Role
from sqlalchemy import String, Integer, Enum, Column

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable = False)
    name = Column(String(255), nullable = False)
    surname = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False)
    hashed_password = Column(String(255))
    role = Column(Enum(Role))
    