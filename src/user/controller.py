from src.user.dtos import Userschema,LoginSchema
from fastapi import HTTPException,status,Request

from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
from src.utils.settings import settings
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timedelta

password_hash=PasswordHash.recommended()

def get_password_hash(password:str):
    return password_hash.hash(password)

def verify(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)


def register(body:Userschema,db:Session):
    is_user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if is_user:
        raise HTTPException(400,detail="Username alredy exists...")
    
    is_email=db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_email:
        raise HTTPException(400,detail="Email alredy used...")
    
    hash_password=get_password_hash(body.password)
    new_user=UserModel(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(body:LoginSchema,db:Session):
    is_user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong Username ,Please try again ..")
    
    if not verify(body.password,is_user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong Password")

    exp_time=datetime.now() + timedelta(minutes=settings.EXP_TIME)
    print(exp_time)
    token=jwt.encode({"_id":is_user.id,"exp":exp_time.timestamp()},settings.SECRET_KEY,settings.ALGORITHM)
    return {"token":token}





def is_authentication(request:Request,db:Session):
    token=request.headers.get("authorization")
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")
    try:
        token=token.split(" ")[-1]
        data=jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)
        user_id=data.get("_id") 
        is_user=db.query(UserModel).filter(UserModel.id==user_id).first()
        if not is_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")

        return is_user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")

   