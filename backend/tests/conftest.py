"""
Configurações e fixtures compartilhadas para testes
"""

import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime


@pytest.fixture
def mock_supabase_client():
    """Mock do cliente Supabase"""
    client = Mock()
    client.table = Mock()
    return client


@pytest.fixture
def sample_lead_data():
    """Dados de exemplo para um lead"""
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "teste@exemplo.com",
        "nombre": "Lead Teste",
        "created_at": datetime.now().isoformat()
    }


@pytest.fixture
def sample_leads_list(sample_lead_data):
    """Lista de leads de exemplo"""
    return [
        sample_lead_data,
        {
            "id": "223e4567-e89b-12d3-a456-426614174000",
            "email": "teste2@exemplo.com",
            "nombre": "Lead Teste 2",
            "created_at": datetime.now().isoformat()
        }
    ]


@pytest.fixture
def sample_user_data():
    """Dados de exemplo para um usuário"""
    return {
        "id": 1,
        "username": "testuser",
        "email": "user@exemplo.com",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lE3PYqxqvK5u",
        "is_active": True,
        "active": True,  # Campo usado pelo user_service
        "created_at": datetime.now().isoformat()
    }


@pytest.fixture
def sample_newsletter_data():
    """Dados de exemplo para uma newsletter"""
    return {
        "subject": "Newsletter Teste",
        "news_items": [
            {
                "title": "Notícia 1",
                "content": "Conteúdo da notícia 1"
            },
            {
                "title": "Notícia 2",
                "content": "Conteúdo da notícia 2"
            }
        ],
        "theme": "federacion_poker"
    }


@pytest.fixture
def mock_smtp_client():
    """Mock do cliente SMTP"""
    client = AsyncMock()
    client.connect = AsyncMock()
    client.login = AsyncMock()
    client.send_message = AsyncMock()
    client.quit = AsyncMock()
    return client
