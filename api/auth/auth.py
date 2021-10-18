from fastapi import APIRouter, HTTPException, Security
from fastapi.param_functions import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select


from api.auth.helpers import Auth
from api.auth import models
from utils import errors
from core.db import get_db

helper = Auth()

auth = APIRouter()

@auth.post('/signup', response_model=models.UserRead)
def signup(user_in: models.UserCreate, db: Session = Depends(get_db)):
    stmt = select(models.User).where(models.User.email==user_in.email)
    user_db = db.exec(stmt)
    if not user_db:       
        raise errors.user_exits(user_in.email)
    
    try:
        hash = helper.encode_password(user_in.password)
        user_in.password = hash
        user = models.User.from_orm(user_in)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except:
        error_msg = "Failed to signup user"
        return error_msg