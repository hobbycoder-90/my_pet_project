from pydantic import BaseModel, EmailStr
from typing import List



class UserSchema(BaseModel):
    id: int
    email: EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    hashed_password: str
    
    
class UserResponseSchema(UserSchema):
    hashed_password: str
    
    class Config:
        from_attributes = True


class UserUpdatePasswordSchema(BaseModel):
    hashed_password: str


class UserUpdateEmailSchema(BaseModel):
    email: EmailStr


class UserUpdateSchema(UserUpdateEmailSchema, UserUpdatePasswordSchema):
    pass
