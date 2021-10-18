from datetime import datetime
from pydantic import EmailStr
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    email: EmailStr
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str

class UserRead(UserCreate):
    id: int

class User(UserCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True))
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()
