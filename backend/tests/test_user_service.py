"""
Testes unitários para UserService
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.user_service import UserService
from app.models.auth_schemas import UserCreate, UserUpdate


class TestUserService:
    """Testes para o serviço de usuários"""

    @pytest.fixture
    def service(self, mock_supabase_client):
        """Cria uma instância do serviço com mock"""
        with patch('app.services.user_service.create_client', return_value=mock_supabase_client):
            with patch('app.services.user_service.settings') as mock_settings:
                mock_settings.SUPABASE_URL = "https://test.supabase.co"
                mock_settings.SUPABASE_KEY = "test-key"
                mock_settings.USERS_TABLE = "users_newsletter"
                service = UserService()
                return service

    @pytest.mark.asyncio
    async def test_get_all_users_success(self, service, mock_supabase_client, sample_user_data):
        """Testa busca de todos os usuários"""
        # Arrange
        mock_response = Mock(data=[sample_user_data])
        mock_table = Mock()
        mock_table.select.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_all_users()

        # Assert
        assert len(result) == 1
        assert result[0]["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_get_all_users_empty(self, service, mock_supabase_client):
        """Testa busca de usuários quando não há dados"""
        # Arrange
        mock_response = Mock(data=[])
        mock_table = Mock()
        mock_table.select.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_all_users()

        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_get_user_by_username_found(self, service, mock_supabase_client, sample_user_data):
        """Testa busca de usuário por username encontrado"""
        # Arrange
        mock_response = Mock(data=[sample_user_data])
        mock_table = Mock()
        mock_table.select.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_user_by_username("testuser")

        # Assert
        assert result is not None
        assert result["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_get_user_by_username_not_found(self, service, mock_supabase_client):
        """Testa busca de usuário por username não encontrado"""
        # Arrange
        mock_response = Mock(data=[])
        mock_table = Mock()
        mock_table.select.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_user_by_username("naoexiste")

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_create_user_success(self, service, mock_supabase_client, sample_user_data):
        """Testa criação de usuário com sucesso"""
        # Arrange
        user = UserCreate(
            username="newuser",
            email="new@exemplo.com",
            password="senha123",
            full_name="Novo Usuário",
            is_admin=False
        )

        mock_table = Mock()
        # Mock para verificações de existência (não existe)
        mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[])
        # Mock para inserção
        mock_table.insert.return_value.execute.return_value = Mock(data=[sample_user_data])
        mock_supabase_client.table.return_value = mock_table

        with patch('app.services.user_service.get_password_hash', return_value="hashed_password"):
            # Act
            result = await service.create_user(user)

            # Assert
            assert result is not None
            assert "password_hash" not in result  # Senha não deve ser retornada

    @pytest.mark.asyncio
    async def test_create_user_username_exists(self, service, mock_supabase_client, sample_user_data):
        """Testa criação de usuário com username já existente"""
        # Arrange
        user = UserCreate(
            username="testuser",
            email="new@exemplo.com",
            password="senha123",
            full_name="Novo Usuário",
            is_admin=False
        )

        mock_table = Mock()
        # Retorna usuário existente na primeira chamada (verificação de username)
        mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[sample_user_data])
        mock_supabase_client.table.return_value = mock_table

        # Act & Assert
        with pytest.raises(ValueError, match="Username já existe"):
            await service.create_user(user)

    @pytest.mark.asyncio
    async def test_create_user_email_exists(self, service, mock_supabase_client, sample_user_data):
        """Testa criação de usuário com email já existente"""
        # Arrange
        user = UserCreate(
            username="newuser",
            email="user@exemplo.com",
            password="senha123",
            full_name="Novo Usuário",
            is_admin=False
        )

        mock_table = Mock()
        # Primeira chamada (username) retorna vazio
        # Segunda chamada (email) retorna usuário existente
        mock_table.select.return_value.eq.return_value.execute.side_effect = [
            Mock(data=[]),  # Username não existe
            Mock(data=[sample_user_data])  # Email existe
        ]
        mock_supabase_client.table.return_value = mock_table

        # Act & Assert
        with pytest.raises(ValueError, match="Email já existe"):
            await service.create_user(user)

    @pytest.mark.asyncio
    async def test_update_user_success(self, service, mock_supabase_client, sample_user_data):
        """Testa atualização de usuário com sucesso"""
        # Arrange
        user_id = "1"
        user_update = UserUpdate(email="newemail@exemplo.com", full_name="Nome Atualizado")

        mock_table = Mock()
        # Mock para verificação de email
        mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[])
        # Mock para update
        updated_data = sample_user_data.copy()
        updated_data["email"] = "newemail@exemplo.com"
        mock_table.update.return_value.eq.return_value.execute.return_value = Mock(data=[updated_data])
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.update_user(user_id, user_update)

        # Assert
        assert result is not None
        assert result["email"] == "newemail@exemplo.com"

    @pytest.mark.asyncio
    async def test_update_user_no_fields(self, service, mock_supabase_client):
        """Testa atualização de usuário sem campos"""
        # Arrange
        user_id = "1"
        user_update = UserUpdate()  # Todos os campos None

        # Act & Assert
        with pytest.raises(ValueError, match="Nenhum campo para atualizar"):
            await service.update_user(user_id, user_update)

    @pytest.mark.asyncio
    async def test_delete_user_success(self, service, mock_supabase_client, sample_user_data):
        """Testa deleção de usuário com sucesso"""
        # Arrange
        user_id = "1"
        mock_response = Mock(data=[sample_user_data])
        mock_table = Mock()
        mock_table.delete.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.delete_user(user_id)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, service, mock_supabase_client):
        """Testa deleção de usuário não encontrado"""
        # Arrange
        user_id = "999"
        mock_response = Mock(data=[])
        mock_table = Mock()
        mock_table.delete.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.delete_user(user_id)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, service, mock_supabase_client, sample_user_data):
        """Testa autenticação de usuário com sucesso"""
        # Arrange
        username = "testuser"
        password = "senha123"

        mock_table = Mock()
        mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[sample_user_data])
        mock_supabase_client.table.return_value = mock_table

        with patch('app.services.user_service.verify_password', return_value=True):
            # Act
            result = await service.authenticate_user(username, password)

            # Assert
            assert result is not None
            assert result["username"] == "testuser"
            assert "password_hash" not in result

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, service, mock_supabase_client, sample_user_data):
        """Testa autenticação com senha incorreta"""
        # Arrange
        username = "testuser"
        password = "senha_errada"

        mock_table = Mock()
        mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[sample_user_data])
        mock_supabase_client.table.return_value = mock_table

        with patch('app.services.user_service.verify_password', return_value=False):
            # Act
            result = await service.authenticate_user(username, password)

            # Assert
            assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_user_not_active(self, service, mock_supabase_client, sample_user_data):
        """Testa autenticação de usuário inativo"""
        # Arrange
        username = "testuser"
        password = "senha123"
        inactive_user = sample_user_data.copy()
        inactive_user["is_active"] = False
        inactive_user["active"] = False  # Campo usado pelo user_service

        mock_table = Mock()
        mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[inactive_user])
        mock_supabase_client.table.return_value = mock_table

        with patch('app.services.user_service.verify_password', return_value=True):
            # Act
            result = await service.authenticate_user(username, password)

            # Assert
            assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(self, service, mock_supabase_client):
        """Testa autenticação de usuário não encontrado"""
        # Arrange
        username = "naoexiste"
        password = "senha123"

        mock_table = Mock()
        mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[])
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.authenticate_user(username, password)

        # Assert
        assert result is None
