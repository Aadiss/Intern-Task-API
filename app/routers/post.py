from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode, user
from app import models
from typing import List

from app.database import get_db
from .. import schemas

from .. import auth

auth_handler = auth.AuthHandler()

router = APIRouter(
    prefix="/message",
    tags=["posts"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.DisplayMessage)
def create_post(post: schemas.PostMessage, db: Session = Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    if 161 > len(post.content) > 0:
        new_post = models.Post(content=post.content, owner_id = username)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid length")

@router.get("/all", response_model=List[schemas.DisplayMessage])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content not found")

    for post in posts:
        post.counter += 1
        db.commit()
        db.refresh(post)

    return posts

@router.get("/{id}", response_model=schemas.DisplayMessage)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.counter += 1
    db.commit()
    db.refresh(post)

    return post


@router.put("/{id}", response_model=schemas.DisplayMessage)
def update_post_by_id(id: int, new_content: str, db: Session = Depends(get_db), username = Depends(auth_handler.auth_wrapper)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content not found")
    
    if post.owner_id != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="That post does not belong to you!")

    post.content = new_content
    post.counter = 0
    db.commit()
    db.refresh(post)

    return post
    

@router.delete("/{id}")
def delete_message(id: int, db: Session = Depends(get_db), username = Depends(auth_handler.auth_wrapper)):
    message = db.query(models.Post).filter(models.Post.id == id).first()

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content not found")
    
    if message.owner_id != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="That post does not belong to you!")

    db.delete(message)
    db.commit()

    return {"info": "deleted"}