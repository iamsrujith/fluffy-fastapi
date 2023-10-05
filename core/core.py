import os
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
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
    otp = str(randint(1000, 9999))
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


@app.post('/validate-otp', description="Creates tokens from validating OTP", tags=['validation'])
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


@app.post('/create-access-token', description="used to create access token refresh token", response_model=dict, tags=['validation'])
async def create_access_token(token: pydantic.RefreshToken, db: Session = Depends(get_db)):
    payload = crypt.verify_refresh_token(token.token)
    if payload:
        number = payload.get('sub')
        user = db.query(User).filter_by(number=number).first()
        if user:
            token = crypt.create_access_token(number)
            return {"access_token": token}
    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    

@app.get('/me', response_model=pydantic.UserData, tags=['user'])
async def get_me(user: pydantic.Users = Depends(get_current_user)):
    user_data = pydantic.UserData(
        number=user.number,
        gender=user.gender,
        location=user.location,
        birthdate=user.birthdate,
        email=user.email,
        full_name=user.full_name,
        gallery=[
            pydantic.UserGallery(name=gallery.name, image_data=gallery.image_data)
            for gallery in user.galleries
        ],
        tag=[
            pydantic.UserTags(tag=tag.tag)
            for tag in user.tags
        ],
    )
    return user_data


@app.put('/update', response_model=pydantic.Users, tags=['user'])
async def update_user(user_data: pydantic.Users, user: pydantic.Users = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    user_db = db.query(User).filter_by(number=user.number).first()

    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user_db, field, value)
    db.commit()
    db.refresh(user_db)
    return user_db


@app.post('/add-gallery', tags=['user'])
async def add_images(data: UploadFile = File(...), db: Session = Depends(get_db), 
                     user: pydantic.Users = Depends(get_current_user)):

    try:
        file_extension = data.filename.split(".")[-1]
        file_name = f"user_{user.id}_{data.filename}.{file_extension}"
        file_path = os.path.join("Gallery", file_name)

        with open(file_path, "wb") as file:
            file.write(data.file.read())

        user_gallery = models.UserGallery(
            name = file_name,
            image_data = file_path,
            owner = user
        )
        db.add(user_gallery)
        db.commit()
        db.refresh(user_gallery)
        return {"success": "image has been uploaded"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving the image"
        )


@app.post("/add-tag", tags=['user'])
async def add_tag(data: pydantic.UserTags, db: Session = Depends(get_db),
                  user: pydantic.Users = Depends(get_current_user)):
    if data.tag:
        try:
            for tag_name in data.tag:
                tag = models.UserTag(tag= tag_name, owner_id= user.id)
                db.add(tag)
            db.commit()
            return {"success": "Tags added successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Error adding tags: {str(e)}"
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="No Tags provided"
        )
            
