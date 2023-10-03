from fastapi import FastAPI, Depends, HTTPException, status
from database.models import User
from database.manager import engine, SessionLocal
from sqlalchemy.orm import Session
from random import randint
from database import pydantic, models
from managers import crypt
from database.manager import get_db
from managers.token import get_current_user


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def generate_otp():
    otp = str(randint(1000,9999))
    hashed_otp = crypt.get_password_hash(otp)
    return otp, hashed_otp


def create_user(data: int, db: Session = Depends(get_db)):
    otp, hashed_otp = generate_otp()
    user = User(number=data, otp=hashed_otp)
    print(otp)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, otp


def get_user(data: str, db: Session):
    user = db.query(User).filter_by(number=data).first()
    if not user:
        return False
    return user


@app.post('/validate-number', tags=['validation'])
async def validate_number(data: pydantic.UserRegistration, db: Session = Depends(get_db)):
    user = get_user(data.number, db)
    if user:
        otp, hashed_otp = generate_otp()
        user.otp = hashed_otp
        print(otp)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="OTP has been send sucessfully"
        )
    else:
        user = create_user(data.number, db)
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="OTP Has been send sucessfully"
        )


@app.post('/validate-otp',description="Creates tokens from validating OTP", tags=['validation'])
async def validate_otp(data: pydantic.ValidateOTP, db: Session = Depends(get_db)):
    otp = data.otp
    if otp:
        user = get_user(data.number, db)
        if user and crypt.verify_password(otp, user.otp):
            return {
                "access_token": crypt.create_access_token(user.number),
                "refresh_token": crypt.create_refresh_token(user.number),
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect OTP"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="OTP not found"
        )
    

@app.get('/me', response_model=pydantic.Users, tags=['user'])
async def get_me(user: pydantic.Users = Depends(get_current_user)):
    return user


@app.put('/me', response_model=pydantic.Users, tags=['user'])
async def update_user(user_data: pydantic.Users, user: pydantic.Users = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    user_db = db.query(User).filter_by(number=user.number).first()
    
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    for field, value in user_data.model_dump().items():
        setattr(user_db, field, value)
    db.commit()
    db.refresh(user_db)
    return user_db