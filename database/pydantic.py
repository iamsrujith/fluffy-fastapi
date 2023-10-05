from datetime import datetime,date
from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List


class UserGallery(BaseModel):
    name: str
    image_data: str


class UserTags(BaseModel):
    tag: str


class UserData(BaseModel):
    number: constr(pattern=r'^\+\d{1,15}$', min_length=6, max_length=16)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    birthdate: Optional[date] = None
    location: Optional[str] = None
    gender: Optional[str] = None
    gallery: List[UserGallery]
    tag: List[UserTags] = None


class Users(BaseModel):
    number: Optional[constr(pattern=r'^\+\d{1,15}$', min_length=6, max_length=16)] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    birthdate: Optional[date] = None
    location: Optional[str] = None
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