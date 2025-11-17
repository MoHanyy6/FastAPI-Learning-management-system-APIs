from pydantic  import BaseModel,EmailStr
from pydantic.types import conint
from datetime import datetime, timezone
from typing import Optional,List

class UserBase(BaseModel):
    name:str
    email:EmailStr
    
    role: Optional[str] = "student"  # default role if not provided

class UserCreate(UserBase):
    password:str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None