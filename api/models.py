from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String

from sqlmodel import Field, SQLModel

# #############################################################################
# Pydantic Schemas
# #############################################################################


class BaseModel(SQLModel):
    name: str


class DepartmentCreate(BaseModel):
    code: str


class DepartmentRead(DepartmentCreate):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


# #############################################################################
# Database tables
# #############################################################################


class Department(DepartmentCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    code: str = Field(sa_column=Column("code", String(2), unique=True))
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()
