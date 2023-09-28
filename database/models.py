from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
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
    profile_picture = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed = Column(Boolean, default=False)



    



