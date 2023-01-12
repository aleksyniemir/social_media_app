from sqlalchemy import String, Integer, Enum, Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
#from src.db.database import Base
from sqlalchemy.orm import declarative_base
#from src.models.friends import friends_association_table 

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    role = Column(String(255), nullable = False, unique = True)
    users = relationship("User", backref="role")
    
friends_association_table = Table(
    "friends_association_table",
    Base.metadata,
    Column("user_a_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("user_b_id", Integer,  ForeignKey("users.id"), primary_key=True)    
)

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
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable = False, unique=True)
    name = Column(String(255), nullable = False)
    surname = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False, unique=True)
    hashed_password = Column(String(255))
    
    friends = relationship("User",
                          secondary = friends_association_table ,
                          primaryjoin = (id == friends_association_table.c.user_a_id),
                          secondaryjoin = (id == friends_association_table.c.user_b_id)
                          )


    role_id = Column(Integer, ForeignKey(Role.id), nullable = False)
    
    groups = relationship(
        "Group", secondary=users_groups_association_table, back_populates="users"
    )
    
    posts = relationship("Post", back_populates="user")
    

    



     