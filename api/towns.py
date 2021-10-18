from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from api import models
from utils import errors
from core.db import get_db

towns = APIRouter()

@towns.get('/', response_model=List[models.TownRead])
def list_towns(db: Session = Depends(get_db)):
    towns = db.exec(select(models.Town)).all()
    return towns


@towns.post('/{department_id}', response_model=models.TownRead)
def create_town(*, db: Session = Depends(get_db), department_id: int, town: models.TownCreate):
    department = db.get(models.Department, department_id)
    if not department:
        raise errors.not_found("Department", department_id)
    print(department)
    town = models.Town.from_orm(town)
    town.department = department

    db.add(town)
    db.commit()
    db.refresh(town)
    return town



@towns.get('/{id}', response_model=models.TownRead)
def read_town(id: int, db: Session = Depends(get_db)):    
    stmt = select(models.Town).where(models.Town.id == id)
    town = db.exec(stmt).first()
    if not town:
        raise errors.not_found("Town", id)
    return town



@towns.patch('/{id}', response_model=models.TownRead)
def update_town(id: int, town: models.TownUpdate, db: Session = Depends(get_db)):
    db_town = db.get(models.Town, id)
    if not db_town:
        raise errors.not_found("Town", id)
    town_data = town.dict(exclude_unset=True)
    for key, value in town_data.items():
        setattr(db_town, key, value)
    db.add(db_town)
    db.commit()
    db.refresh(db_town)
    return db_town


@towns.delete('/{id}')
def delete_town(id: int, db: Session = Depends(get_db)):
    town = db.get(models.Town, id)
    if not town:
        raise errors.not_found("Town", id)
    db.delete(town)
    db.commit()
    return {"ok": True}