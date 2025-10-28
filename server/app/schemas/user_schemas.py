from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import uuid
import re
from models.user_model import User

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User
    
class TokenData(BaseModel):
    id: str | None = None
    role: str | None = None
    email: str | None = None

class UserResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True

class UserRegistrationRequest(BaseModel):
    first_name: str = Field(..., max_length=150)
    last_name: str = Field(..., max_length=150)
    email: str = Field(..., max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("email")
    def validate_email(cls, v):
        if v is None:
            return v
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format.")
        return v

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        pattern = r"^\+?[0-9\-\s\(\)]+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format.")
        return v

class UserLoginRequest(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("email")
    def validate_email(cls, v):
        if v is None:
            return v
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format.")
        return v

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)

    @field_validator("email")
    def validate_email(cls, v):
        if v is None:
            return v
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format.")
        return v
    