from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from fastapi.security import HTTPAuthorizationCredentials

from api.lands import models
from api.auth.auth import secure
from utils import errors
from core.db import get_db

departments = APIRouter()


@departments.get('', response_model=List[models.DepartmentRead])
def list_departments(db: Session = Depends(get_db)):
    departments = db.exec(select(models.Department)).all()
    return  departments


@departments.post('/', response_model=models.DepartmentRead)
def create_department(
        *, 
        db: Session = Depends(get_db), 
        department: models.DepartmentCreate,
        credentials: HTTPAuthorizationCredentials = secure()
    ):
    department = models.Department.from_orm(department)
    db.add(department)
    db.commit()
    db.refresh(department)
    return  department

@departments.get("/{id}", response_model=models.DepartmentRead)
def read_department(id: int, db: Session = Depends(get_db)):    
    stmt = select(models.Department).where(models.Department.id == id)
    department = db.exec(stmt).first()
    if not department:
        raise errors.not_found("Department", id)
    return department


@departments.patch('/{id}')
def update_department(
        id: int, 
        department: models.DepartmentUpdate,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = secure()
    ):
    db_department = db.get(models.Department, id)
    if not db_department:
        raise errors.not_found("Department", id)
    department_data = department.dict(exclude_unset=True)
    for key, value in department_data.items():
        setattr(db_department, key, value)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@departments.delete('/{id}')
def delete_department(
        id: int, 
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = secure()
    ):
    department = db.get(models.Department, id)
    if not department:
        raise errors.not_found("Department", id)
    db.delete(department)
    db.commit()
    return {"ok": True}