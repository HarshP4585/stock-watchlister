from fastapi import Depends, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import time
from .database import get_db
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "de7130244b603febec8439c291764d296bcf46b0d4f880ecbc213804ff1cb95b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_TIME = 60

def get_token(payload: dict):
    payload_copy = payload.copy()
    expire = time.time() + ACCESS_TOKEN_EXPIRATION_TIME * 60
    # use "exp" to use library's expiry time validation
    payload_copy["expire"] = expire
    
    return jwt.encode(payload_copy, SECRET_KEY, ALGORITHM)

def verify_access_token(token: str):
    # how expire will work?
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        
        # verify the expiry of the token
        if payload.get("expire", -1) < time.time():
            raise JWTError("token expired")
        
    except JWTError:
        # return -1
        return -1

    user_id = payload.get("user_id")
    
    if not user_id:
        # return -1
        return -1
    
    # return user_id
    return user_id

# embeded as dependency in controllers to verify token and get user id
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # if token is revoked, return None which will raise error and not let user to access the resources
    # db_token = db.query(RevokedToken).filter(RevokedToken.token == token).first()
    # if db_token:
    #     return None
    
    token = verify_access_token(token)
    # fetch and return user from the database using user id
    user = db.query(User).filter(User.id == token).first()
    return user
