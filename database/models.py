from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Relationship
from database.manager import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, index= True)
    number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    otp = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed = Column(Boolean, default=False)
    galleries = Relationship("UserGallery", back_populates="owner")
    tags = Relationship("UserTag", back_populates="owner")


class UserGallery(Base):
    __tablename__ = "gallery"
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, index=True)
    image_data = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner =  Relationship("User", back_populates="galleries")
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserTag(Base):
    __tablename__ = "usertags"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = Relationship("User", back_populates="tags")




    



