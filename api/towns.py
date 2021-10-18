from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from api import models
from core.db import get_db

towns = APIRouter()

@towns.get('/towns/', response_model=List[models.TownRead])
def list_towns(db: Session = Depends(get_db)):
    towns = db.exec(select(models.Town)).all()
    return towns


@towns.post('/towns/{code}', response_model=models.TownRead)
def create_town(*, db: Session = Depends(get_db), code: str, town: models.TownCreate):
    dep_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Department with code {code} is not available :("
    )

    statement = select(models.Department).where(models.Department.code == code)
    department = db.exec(statement).first()
    if not department:
        raise dep_not_found
    
    town = models.Town.from_orm(town)
    town.department = department

    db.add(town)
    db.commit()
    db.refresh(town)
    return town



@towns.get('/towns/{code}', response_model=models.TownRead)
def read_town(code: str, db: Session = Depends(get_db)):
    town_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Town with code {code} is not available :("
    )

    stmt = select(models.Town).where(models.Town.code == code)
    town = db.exec(stmt).first()
    if not town:
        raise town_not_found
    return town
