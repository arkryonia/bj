from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from api import models
from core.db import get_db

districts = APIRouter()


@districts.get('/')
def list_districts(db: Session = Depends(get_db)):
    return {"message": "this feature is coming..."}


@districts.post('/')
def create_district(district: models.District, db: Session = Depends(get_db)):
    return {"message": "this feature is coming..."}


@districts.patch('/{id}')
def update_district(id: int, district: models.District, db: Session = Depends(get_db)):
    return {"message": "this feature is coming..."}


@districts.delete('/{id}')
def delete_district(id: int, db: Session = Depends(get_db)):
    return {"message": "this feature is coming..."}