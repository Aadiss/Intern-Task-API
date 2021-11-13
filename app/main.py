from fastapi import FastAPI
from .routers import post, user
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "posts",
        "description": "Manage posts. So _fancy_ they have their own docs.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(post.router)
app.include_router(user.router)