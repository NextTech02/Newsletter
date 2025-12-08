"""
Modelos Pydantic para validação de dados
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ============================================================================
# LEADS
# ============================================================================

class LeadBase(BaseModel):
    """Base para Lead"""
    email: EmailStr
    nome: Optional[str] = None


class LeadCreate(LeadBase):
    """Schema para criar Lead"""
    pass


class Lead(LeadBase):
    """Schema de Lead completo"""
    id: str  # UUID como string
    subscribed: Optional[bool] = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LeadsList(BaseModel):
    """Lista de leads"""
    total: int
    leads: List[Lead]


class UnsubscribeRequest(BaseModel):
    """Schema para cancelar inscrição"""
    email: EmailStr
    reason: str = Field(..., min_length=1, description="Motivo do cancelamento")
    comments: Optional[str] = Field(None, description="Comentários adicionais")


# ============================================================================
# NEWSLETTER
# ============================================================================

class NewsItem(BaseModel):
    """Item de notícia"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class NewsletterCreate(BaseModel):
    """Schema para criar Newsletter"""
    subject: str = Field(..., min_length=1, max_length=200, description="Assunto da newsletter")
    news_items: List[NewsItem] = Field(..., min_length=1, description="Lista de notícias")
    theme: Optional[str] = Field(default="federacion_poker", description="Tema visual")


class NewsletterPreview(BaseModel):
    """Preview da newsletter"""
    html: str


class EmailSendRequest(BaseModel):
    """Requisição para enviar email"""
    subject: str
    html_content: str
    recipients: Optional[List[EmailStr]] = None  # Se None, envia para todos os leads
    is_test: bool = False  # Se True, envia apenas para o remetente


class EmailSendResponse(BaseModel):
    """Resposta do envio de email"""
    success: bool
    total_sent: int
    total_failed: int
    message: str
    errors: Optional[List[str]] = None


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class MessageResponse(BaseModel):
    """Resposta genérica com mensagem"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Resposta de erro"""
    detail: str
    error_type: Optional[str] = None
