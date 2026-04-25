from pydantic import BaseModel,HttpUrl,EmailStr #for website,email
from typing import  Optional


#define the body schema 
class Student_Create(BaseModel):
    name: str
    id: int
    dept: str
    sem: int
    email : EmailStr


class Student_Response(BaseModel):
    name: str
    id: int
    dept: str
    sem: int
    email: EmailStr


    class Config:
        from_attributes = True


#new table for stoners

class Stoner_Create(BaseModel):
    name: str
    id: int
    sem: int
    email : EmailStr
    password : str

class Stoner_Response(BaseModel):
    name: str
    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str | int] = None



