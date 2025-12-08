"""
Testes unitários para Auth Service
"""

import pytest
from datetime import timedelta
from unittest.mock import patch
from app.services import auth_service
from app.models.auth_schemas import TokenData


class TestAuthService:
    """Testes para o serviço de autenticação"""

    def test_get_password_hash(self):
        """Testa geração de hash de senha"""
        # Arrange
        password = "senha_teste_123"

        # Act
        hashed = auth_service.get_password_hash(password)

        # Assert
        assert hashed is not None
        assert hashed != password
        assert hashed.startswith("$2b$")  # bcrypt hash prefix

    def test_verify_password_correct(self):
        """Testa verificação de senha correta"""
        # Arrange
        password = "senha_teste_123"
        hashed = auth_service.get_password_hash(password)

        # Act
        result = auth_service.verify_password(password, hashed)

        # Assert
        assert result is True

    def test_verify_password_incorrect(self):
        """Testa verificação de senha incorreta"""
        # Arrange
        password = "senha_teste_123"
        wrong_password = "senha_errada"
        hashed = auth_service.get_password_hash(password)

        # Act
        result = auth_service.verify_password(wrong_password, hashed)

        # Assert
        assert result is False

    def test_verify_password_empty(self):
        """Testa verificação com senha vazia"""
        # Arrange
        password = "senha_teste_123"
        hashed = auth_service.get_password_hash(password)

        # Act
        result = auth_service.verify_password("", hashed)

        # Assert
        assert result is False

    def test_create_access_token_default_expiration(self):
        """Testa criação de token com expiração padrão"""
        # Arrange
        data = {"sub": "testuser", "user_id": 1}

        with patch('app.services.auth_service.settings') as mock_settings:
            mock_settings.SECRET_KEY = "test-secret-key"
            mock_settings.ALGORITHM = "HS256"
            mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30

            # Act
            token = auth_service.create_access_token(data)

            # Assert
            assert token is not None
            assert isinstance(token, str)
            assert len(token) > 0

    def test_create_access_token_custom_expiration(self):
        """Testa criação de token com expiração customizada"""
        # Arrange
        data = {"sub": "testuser", "user_id": 1}
        expires_delta = timedelta(minutes=15)

        with patch('app.services.auth_service.settings') as mock_settings:
            mock_settings.SECRET_KEY = "test-secret-key"
            mock_settings.ALGORITHM = "HS256"

            # Act
            token = auth_service.create_access_token(data, expires_delta)

            # Assert
            assert token is not None
            assert isinstance(token, str)

    def test_verify_token_valid(self):
        """Testa verificação de token válido"""
        # Arrange
        data = {"sub": "testuser", "user_id": "1"}  # user_id deve ser string

        with patch('app.services.auth_service.settings') as mock_settings:
            mock_settings.SECRET_KEY = "test-secret-key"
            mock_settings.ALGORITHM = "HS256"
            mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30

            token = auth_service.create_access_token(data)

            # Act
            token_data = auth_service.verify_token(token)

            # Assert
            assert token_data is not None
            assert isinstance(token_data, TokenData)
            assert token_data.username == "testuser"
            assert token_data.user_id == "1"  # user_id é string

    def test_verify_token_invalid(self):
        """Testa verificação de token inválido"""
        # Arrange
        invalid_token = "token.invalido.aqui"

        with patch('app.services.auth_service.settings') as mock_settings:
            mock_settings.SECRET_KEY = "test-secret-key"
            mock_settings.ALGORITHM = "HS256"

            # Act
            token_data = auth_service.verify_token(invalid_token)

            # Assert
            assert token_data is None

    def test_verify_token_expired(self):
        """Testa verificação de token expirado"""
        # Arrange
        data = {"sub": "testuser", "user_id": 1}
        # Expira em -1 minuto (já expirado)
        expires_delta = timedelta(minutes=-1)

        with patch('app.services.auth_service.settings') as mock_settings:
            mock_settings.SECRET_KEY = "test-secret-key"
            mock_settings.ALGORITHM = "HS256"

            token = auth_service.create_access_token(data, expires_delta)

            # Act
            token_data = auth_service.verify_token(token)

            # Assert
            assert token_data is None

    def test_verify_token_wrong_secret(self):
        """Testa verificação de token com chave secreta diferente"""
        # Arrange
        data = {"sub": "testuser", "user_id": 1}

        with patch('app.services.auth_service.settings') as mock_settings:
            mock_settings.SECRET_KEY = "test-secret-key"
            mock_settings.ALGORITHM = "HS256"
            mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30

            token = auth_service.create_access_token(data)

            # Mudar a chave secreta
            mock_settings.SECRET_KEY = "different-secret-key"

            # Act
            token_data = auth_service.verify_token(token)

            # Assert
            assert token_data is None

    def test_verify_token_missing_sub(self):
        """Testa verificação de token sem campo 'sub'"""
        # Arrange
        data = {"user_id": 1}  # Sem 'sub'

        with patch('app.services.auth_service.settings') as mock_settings:
            mock_settings.SECRET_KEY = "test-secret-key"
            mock_settings.ALGORITHM = "HS256"
            mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30

            token = auth_service.create_access_token(data)

            # Act
            token_data = auth_service.verify_token(token)

            # Assert
            assert token_data is None

    def test_password_hash_different_each_time(self):
        """Testa que o mesmo password gera hashes diferentes (salt)"""
        # Arrange
        password = "senha_teste_123"

        # Act
        hash1 = auth_service.get_password_hash(password)
        hash2 = auth_service.get_password_hash(password)

        # Assert
        assert hash1 != hash2
        # Mas ambos devem verificar corretamente
        assert auth_service.verify_password(password, hash1)
        assert auth_service.verify_password(password, hash2)
