from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from .role import RoleResponse


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="User Name")
    surname: str = Field(..., min_length=1, max_length=100,
                         description="User Surname")
    secondname: Optional[str] = Field(None, min_length=1, max_length=100,
                                      description="User SecondName")


class UserCreate(UserBase):
    email: str = Field(..., min_length=5, max_length=100,
                       description="User email")
    password: str = Field(..., min_length=8, max_length=50,
                          description="User Password")
    role_id: int = Field(..., description="User's Role ID")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100,
                                description="User Name")
    surname: Optional[str] = Field(None, min_length=1, max_length=100,
                                   description="User Surname")
    secondname: Optional[str] = Field(None, min_length=1, max_length=100,
                                      description="User SecondName")
    email: Optional[str] = Field(None, min_length=5, max_length=100,
                                 description="User email")


class UserResponse(BaseModel):
    id: int = Field(..., description="Unique User ID")
    name: str
    surname: str
    secondname: Optional[str]
    email: str
    role_id: int
    is_active: bool
    role: Optional[RoleResponse] = Field(None, description="User Role")

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User Password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
