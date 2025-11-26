from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class URL(BaseModel):
    id: int
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True
