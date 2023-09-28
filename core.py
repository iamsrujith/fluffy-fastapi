from fastapi import FastAPI, Depends
from database.models import User
from database.manager import engine, SessionLocal
from sqlalchemy.orm import Session
import hashlib
from random import randint
from database.pydantic import UserRegistration
from database import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def generate_otp():
    otp = str(randint(1000,9999))
    hashed_otp = hashlib.sha256(otp.encode()).hexdigest()
    return otp, hashed_otp


def create_user(data: int, db: Session = Depends(get_db)):
    otp, hashed_otp = generate_otp()
    user = User(number=data, otp=hashed_otp)
    print(otp)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, otp

@app.post('/validate-number')
async def validate_number(data: UserRegistration, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(number=data.number).first()
    if user:
        otp, hashed_otp = generate_otp()
        user.otp = hashed_otp
        print(otp)
        db.commit()
        return {"success": "OTP send sucessfully"}
    else:
        user = create_user(data.number, db)
        print(user[1])
        return {"sucess": " account created OTP send sucessfully"}
        
