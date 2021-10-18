from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean

from sqlmodel import Field, SQLModel, Relationship

# #############################################################################
# Pydantic Schemas
# #############################################################################


class DepartmentCreate(SQLModel):
    name: str


class TownCreate(SQLModel):
    name: str
    is_capital: Optional[bool] = False


class DepartmentRead(DepartmentCreate):
    id: int
    towns: Optional[List[TownCreate]] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class TownDepartmentRead(DepartmentCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TownRead(TownCreate):
    id: int
    department: Optional[TownDepartmentRead] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class DistrictCreate(SQLModel):
    name: str


class DistrictRead(DistrictCreate):
    id: int
    town: Optional[TownDepartmentRead] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class DistrictUpdate(SQLModel):
    name: Optional[str] = None
    town_id: Optional[int] = None

# #############################################################################
# Database tables
# #############################################################################


class Department(DepartmentCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()

    towns: List["Town"] = Relationship(back_populates="department")


class Town(TownCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    is_capital: bool = Field(sa_column=Column("is_capital", Boolean, default=False))
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()

    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    department: Optional[Department] = Relationship(back_populates="towns")

    districts: List["District"] = Relationship(back_populates="town")


class District(DistrictCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()

    town_id: Optional[int] = Field(default=None, foreign_key="town.id")
    town: Optional[Town] = Relationship(back_populates="districts")
