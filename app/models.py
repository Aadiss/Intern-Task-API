from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(length=160), nullable=False)
    counter = Column(Integer, server_default="0")
    owner_id = Column(Integer, ForeignKey('users.id'))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), nullable=False)
    password = Column(String(length=200), nullable=False)
