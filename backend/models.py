from sqlalchemy import Column, Integer, String, Boolean, ARRAY, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, validates
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    isAdmin = Column(Boolean, default=False)
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False)
    skills = relationship("Skill", back_populates="user")


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    interestedIn = Column(ARRAY(String), nullable=True)

    # Back-populates
    user = relationship("Users", back_populates="profile")


class Skill(Base):
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    level = Column(Integer, CheckConstraint('level >= 1 AND level <= 10'), nullable=False)
    priority = Column(Integer, CheckConstraint('priority > 0'), nullable=False)

    # Back-populates
    user = relationship("Users", back_populates="skills")

    @validates('level')
    def validate_level(self, key, value):
        if not (1 <= value <= 10):
            raise ValueError("Level must be between 1 and 10.")
        return value

    @validates('priority')
    def validate_priority(self, key, value):
        if value <= 0:
            raise ValueError("Priority must be a positive integer.")
        return value
