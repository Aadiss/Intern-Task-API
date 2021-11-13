from pydantic import BaseModel

class PostMessage(BaseModel):
    content: str

class DisplayMessage(BaseModel):
    content: str
    counter: int

    class Config:
        orm_mode = True

class AuthDetails(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True