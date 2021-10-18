from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from api import models
from core.db import get_db

districts = APIRouter()

def not_found(obj: str, id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{obj} with id {id} is not available :("
    )

@districts.get('/', response_model=List[models.DistrictRead])
def list_districts(db: Session = Depends(get_db)):
    districts = db.exec(select(models.District)).all()
    return districts


@districts.post('/{town_id}', response_model=models.DistrictRead)
def create_district(town_id: int, district: models.DistrictCreate, db: Session = Depends(get_db)):
    
    town = db.get(models.Town, town_id)
    if not town:
        raise not_found("Town", town_id)
    
    district = models.District.from_orm(district)
    district.town = town
    db.add(district)
    db.commit()
    db.refresh(district)
    return district


@districts.patch('/{id}', response_model=models.DistrictRead)
def update_district(id: int, district: models.DistrictUpdate, db: Session = Depends(get_db)):
    print("yes yes yes")
    db_district = db.get(models.District, id)
    if not db_district:
        raise not_found("District", id)
    district_data = district.dict(exclude_unset=True)
    for key, value in district_data.items():
        setattr(db_district, key, value)
    db.add(db_district)
    db.commit()
    db.refresh(db_district)    
    return db_district


@districts.delete('/{id}',)
def delete_district(id: int, db: Session = Depends(get_db)):
    db_district = db.get(models.District, id)
    if not db_district:
        raise not_found("District", id)
    db.delete(db_district)
    db.commit()
    return {"ok": True}