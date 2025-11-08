# app/oAuth2.py
from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,database, tablesmodel
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

"""
data = {"user_id": id, "role": "user" or "admin"}
"""
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id = payload.get("user_id")
        role = payload.get("role")

        if id is None:
           raise credentials_exception
        
        token_data = schemas.TokenData(id = str(id), role = role)

    except JWTError:
        raise credentials_exception 
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    
    token_data = verify_access_token(token, credentials_exception)
    try:
        user_id = int(token_data.id)
    except Exception:
        raise credentials_exception

    user = db.query(tablesmodel.User).filter(tablesmodel.User.id == user_id).first()
    if not user:
        raise credentials_exception
    return user

def require_admin(current_user: tablesmodel.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user