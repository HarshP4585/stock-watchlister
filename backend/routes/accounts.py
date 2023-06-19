import json
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from ..dto import Login, Register
from ..database import get_db
from ..models import User as UserSQLAlchemy
from ..utils import hash, verify
from ..oauth2 import get_token

router = APIRouter()

@router.post("/login")
def login(payload: Login, db: Session = Depends(get_db)):
    user = db.query(UserSQLAlchemy).filter(UserSQLAlchemy.email == payload.email).first()
    if not user:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=json.dumps({"detail": "User does not exist"}),
            media_type="application/json"
        )
    elif not verify(payload.password, user.password):
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=json.dumps({"detail": "Incorrect password"}),
            media_type="application/json"
        )
    access_token = get_token({"user_id": user.id})
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps({"detail": {"access_token": access_token, "token_type": "Bearer"}}),
        media_type="application/json"
    )

@router.post("/register")
def register(payload: Register, db: Session = Depends(get_db)):
    user = db.query(UserSQLAlchemy).filter(UserSQLAlchemy.email == payload.email).first()
    if user:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=json.dumps({"detail": "User already exists"}),
            media_type="application/json"
        )
    user = UserSQLAlchemy(**payload.dict())
    user.password = hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return Response(
        status_code=status.HTTP_201_CREATED
    )
