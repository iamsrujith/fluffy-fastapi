from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from database.manager import get_db
from database.models import User
from managers.crypt import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from pydantic import ValidationError
from database.pydantic import Users, ValidateOTP, TokenPayload
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/validate-otp",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth), 
                           db: Session = Depends(get_db)) -> ValidateOTP:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user: Union[dict[str, Any], None] = db.query(User).filter_by(number=token_data.sub).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )
    return user