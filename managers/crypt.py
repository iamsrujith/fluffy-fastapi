from datetime import timedelta, datetime
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "a915f7e4af1a5a804e4ffe5a15b9027ca66a52b152e485f05cdaf34c044d72b4"
REFRESH_TOKEN_SECRET_KEY = "7161c05d364f05ba4b3fede3c3fcdfc051a7520e3317fbb625abcfa573397d06"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
        return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, ALGORITHM)
        return encoded_jwt
