# from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean

from sqlmodel import Field, SQLModel, Relationship

# #############################################################################
# Pydantic Schemas
# #############################################################################


class DepartmentCreate(SQLModel):
    name: str
    code: str


class TownCreate(SQLModel):
    name: str
    code: str
    is_capital: Optional[bool] = False


class DepartmentRead(DepartmentCreate):
    towns: Optional[List[TownCreate]] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TownRead(TownCreate):
    department: Optional[DepartmentRead] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class DistrictCreate(SQLModel):
    name: str


class DistrictRead(DistrictCreate):
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

    towns: List["Town"] = Relationship(back_populates="department")


class Town(TownCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    code: str = Field(sa_column=Column("code", String(2), unique=True))
    is_capital: bool = Field(sa_column=Column("is_capital", Boolean, default=False))
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()

    department_id: Optional[int] = Field(
        default=None, foreign_key="department.id")
    department: Optional[Department] = Relationship(back_populates="towns")

    districts: List["District"] = Relationship(back_populates="town")


class District(DistrictCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()

    town_id: Optional[int] = Field(default=None, foreign_key="town.id")
    town: Optional[Town] = Relationship(back_populates="districts")
