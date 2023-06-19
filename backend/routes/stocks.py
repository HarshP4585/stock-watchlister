import json
from typing import Optional
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from ..dto import WatchList
from ..database import get_db
from ..models import User as UserSQLAlchemy, WatchList as WatchListSQLAlchemy
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/watchlist"
)

@router.post("/add")
def add_to_watchlist(payload: WatchList, db: Session = Depends(get_db), user: Optional[UserSQLAlchemy]= Depends(get_current_user)):
    if not user:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
            content=json.dumps({"detail": "Not authorized"}),
            media_type="application/json"
        )
    watchlist = db.query(WatchListSQLAlchemy).filter(WatchListSQLAlchemy.user_id == user.id)
    watchlist_data = watchlist.first()
    
    if not watchlist_data:
        watchlist = WatchListSQLAlchemy(**{
            "stocks": ";".join(payload.stocks),
            "user_id": user.id
        })
        db.add(watchlist)
        db.commit()
        db.refresh(watchlist)
        return Response(
            status_code=status.HTTP_200_OK,
            content=json.dumps({"detail": watchlist.stocks.split(";")}),
            media_type="application/json"
        )
    
    to_update = set(payload.stocks) | set(watchlist_data.stocks.split(";"))
    watchlist.update({"stocks": ";".join(to_update)})
    db.commit()
    db.refresh(watchlist_data)
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps({"detail": watchlist_data.stocks.split(";")}),
        media_type="application/json"
    )

@router.post("/remove")
def remove_from_watchlist(payload: WatchList, db: Session = Depends(get_db), user: Optional[UserSQLAlchemy]= Depends(get_current_user)):
    if not user:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
            content=json.dumps({"detail": "Not authorized"}),
            media_type="application/json"
        )
    watchlist = db.query(WatchListSQLAlchemy).filter(WatchListSQLAlchemy.user_id == user.id)
    watchlist_data = watchlist.first()
    
    if not watchlist_data:
        return Response(
            status_code=status.HTTP_200_OK,
            content=json.dumps({"detail": []}),
            media_type="application/json"
        )
    
    to_update = set(watchlist_data.stocks.split(";")) - set(payload.stocks)
    watchlist.update({"stocks": ";".join(to_update)})
    db.commit()
    db.refresh(watchlist_data)
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps({"detail": watchlist_data.stocks.split(";")}),
        media_type="application/json"
    )

@router.get("/")
def get_watchlist(db: Session = Depends(get_db), user: Optional[UserSQLAlchemy]= Depends(get_current_user)):
    if not user:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
            content=json.dumps({"detail": "Not authorized"}),
            media_type="application/json"
        )
    watchlist_list = []
    watchlist = db.query(WatchListSQLAlchemy).filter(WatchListSQLAlchemy.user_id == user.id).first()
    if watchlist:
        watchlist_list = watchlist.stocks.split(";")
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps({"detail": watchlist_list}),
        media_type="application/json"
    )

@router.delete("/")
def delete_watchlist(db: Session = Depends(get_db), user: Optional[UserSQLAlchemy]= Depends(get_current_user)):
    if not user:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
            content=json.dumps({"detail": "Not authorized"}),
            media_type="application/json"
        )
    watchlist = db.query(WatchListSQLAlchemy).filter(WatchListSQLAlchemy.user_id == user.id)
    if not watchlist.first():
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=json.dumps({"detail": "No watchlist to delete"}),
            media_type="application/json"
        )
    
    watchlist.delete(synchronize_session=False)
    db.commit()
    
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
