from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# postgresql://user:password@hostname/db
SQLALCHEMY_DATABSE_URL = f"postgresql://postgres:test@localhost:5432/stock-watchlist"

engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
