from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm.session import Session
from app import models
from typing import List

from app.database import get_db
from .. import schemas

from .. import auth

auth_handler = auth.AuthHandler()

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(auth_details: schemas.AuthDetails, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == auth_details.username).first()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username is taken")

    hashed_password = auth_handler.get_password_hash(auth_details.password)

    user = models.User(username=auth_details.username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "registration succesful"}
    

@router.post('/login', status_code=status.HTTP_200_OK)
def login(auth_details: schemas.AuthDetails, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == auth_details.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")

    if not auth_handler.verify_password(auth_details.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid credentials")

    token = auth_handler.ecnode_token(user.id)

    return {"token": token, "info": "token is valid for 10 mins"}