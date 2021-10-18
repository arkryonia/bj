from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from api import models
from core.db import get_db

departments = APIRouter()


@departments.get('', response_model=List[models.DepartmentRead])
def list_departments(db: Session = Depends(get_db)):
    departments = db.exec(select(models.Department)).all()
    return  departments


@departments.post('/', response_model=models.DepartmentRead)
def create_department(*, db: Session = Depends(get_db), department: models.DepartmentCreate):
    department = models.Department.from_orm(department)
    db.add(department)
    db.commit()
    db.refresh(department)
    return  department

@departments.get("/{id}", response_model=models.DepartmentRead)
def read_department(id: int, db: Session = Depends(get_db)):
    dep_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Department with id {id} is not available :("
    )
    stmt = select(models.Department).where(models.Department.id == id)
    department = db.exec(stmt).first()
    if not department:
        raise dep_not_found
    return department


@departments.patch('/{id}')
def update_department(id: int, department: models.Department):
    return {"message": "this feature is coming..."}


@departments.delete('/{id}')
def delete_department(id: int):
    return {"message": "this feature is coming..."}