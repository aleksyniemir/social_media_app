from sqlalchemy import String, Integer, Enum, Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.models.users import Base

users_groups_association_table = Table(
    "users_groups_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("group_id", ForeignKey("groups.id"))    
)

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    
    users = relationship(
        "User", secondary=users_groups_association_table, back_populates="groups"
    )
    
    