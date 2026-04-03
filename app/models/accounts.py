from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(SqlEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    
    profile = relationship("Profile", back_populates="owner", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String, default="Hello world!")
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="profile")
