from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class Users(BaseModel):
    number: constr(pattern=r'^\+\d{1,15}$', min_length=6, max_length=16)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    birthdate: Optional[datetime] = None
    location: Optional[str] = None
    profile_picture: Optional[str] = None
    gender: Optional[str] = None


class UserRegistration(BaseModel):
    number: constr(pattern=r'^\+\d{1,15}$', min_length=6, max_length=16)


class ValidateOTP(BaseModel):
    number: constr(pattern=r'^\+\d{1,15}$', min_length=6, max_length=16)
    otp: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class RefreshToken(BaseModel):
    token: str = None

class UserGallery(BaseModel):
    name: str
    image_data: str
