from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import Base
from .database import engine
from .routes import accounts, stocks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(accounts.router)
app.include_router(stocks.router)
