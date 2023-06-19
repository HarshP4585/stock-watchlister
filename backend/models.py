from sqlalchemy import Column, String, Integer, DateTime, text, ForeignKey
from sqlalchemy.orm import relationship, backref
from .database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    fname = Column(String, nullable=False)
    lname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("NOW()"))

class WatchList(Base):
    __tablename__ = "watchlist"
    
    id = Column(Integer, primary_key=True)
    stocks = Column(String, default="")
    
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", uselist=False)
