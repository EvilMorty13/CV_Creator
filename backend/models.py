from sqlalchemy import Column, Integer, String, Boolean, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from database import *


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    isAdmin = Column(Boolean, default=False)
    
    # Add the relationship here
    profile = relationship("Profile", back_populates="user", uselist=False)


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    name = Column(String, nullable=False)
    interestedIn = Column(ARRAY(String), nullable=True)  

    # Add the back_populates here to link with the Users model
    user = relationship("Users", back_populates="profile")
