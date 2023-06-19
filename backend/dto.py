from typing import List
from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    email: EmailStr
    password: str

class Register(Login):
    fname: str
    lname: str

class WatchList(BaseModel):
    stocks: List[str]
