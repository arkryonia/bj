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

def secure():
    security = HTTPBearer()
    return Security(security)


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


@auth.post('/login')
def login(user_in: models.UserLogin, db: Session = Depends(get_db)):
    print(user_in.password)
    stmt = select(models.User).where(models.User.email==user_in.email)
    user = db.exec(stmt).first()
    if not user:
        return errors.email_error()

    if (not helper.verify_password(user_in.password, user.password)):
        return HTTPException(status_code=401, detail="Invalid password")
    
    if not user.is_active:
        raise errors.disabled_user()

    access_token = helper.encode_token(user.email)
    refresh_token = helper.encode_refresh_token(user.email)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@auth.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = secure()):
    refresh_token = credentials.credentials
    new_token = helper.refresh_token(refresh_token)
    return {'access_token': new_token}
