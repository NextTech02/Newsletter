"""
Schemas de autenticação
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============================================================================
# USER SCHEMAS
# ============================================================================

class UserBase(BaseModel):
    """Base para User"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema para criar User"""
    password: str = Field(..., min_length=6)
    is_admin: bool = False


class UserUpdate(BaseModel):
    """Schema para atualizar User"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)


class User(UserBase):
    """Schema de User completo"""
    id: str
    active: bool = True
    is_admin: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInDB(User):
    """User com hash de senha (apenas para uso interno)"""
    password_hash: str


# ============================================================================
# AUTH SCHEMAS
# ============================================================================

class Token(BaseModel):
    """Token de acesso"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Dados do token"""
    username: Optional[str] = None
    user_id: Optional[str] = None


class LoginRequest(BaseModel):
    """Request de login"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Response de login"""
    access_token: str
    token_type: str = "bearer"
    user: User


# ============================================================================
# USER LIST
# ============================================================================

class UsersList(BaseModel):
    """Lista de usuários"""
    total: int
    users: list[User]
