from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class Users(BaseModel):
    number: constr(pattern=r'^\+\d{1,15}$', min_length=6, max_length=16)
    email: Optional[EmailStr] = None
    otp: Optional[str] = None
    full_name: Optional[str] = None
    birthdate: Optional[datetime] = None
    location: Optional[str] = None
    profile_picture: Optional[str] = None
    gender: Optional[str] = None


class UserRegistration(BaseModel):
    number: constr(pattern=r'^\+\d{1,15}$', min_length=6, max_length=16)