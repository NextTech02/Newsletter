"""
Testes unitários para SupabaseService
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.supabase_service import SupabaseService
from app.models.schemas import LeadCreate


class TestSupabaseService:
    """Testes para o serviço Supabase"""

    @pytest.fixture
    def service(self, mock_supabase_client):
        """Cria uma instância do serviço com mock"""
        with patch('app.services.supabase_service.create_client', return_value=mock_supabase_client):
            with patch('app.services.supabase_service.settings') as mock_settings:
                mock_settings.SUPABASE_URL = "https://test.supabase.co"
                mock_settings.SUPABASE_KEY = "test-key"
                mock_settings.LEADS_TABLE = "newsletter_leads"
                service = SupabaseService()
                return service

    @pytest.mark.asyncio
    async def test_get_all_leads_success(self, service, mock_supabase_client, sample_leads_list):
        """Testa busca de todos os leads com sucesso"""
        # Arrange
        mock_response = Mock()
        mock_response.data = sample_leads_list

        mock_table = Mock()
        mock_table.select.return_value.range.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_all_leads()

        # Assert
        assert len(result) == 2
        assert result[0]["email"] == "teste@exemplo.com"
        assert result[1]["email"] == "teste2@exemplo.com"

    @pytest.mark.asyncio
    async def test_get_all_leads_empty(self, service, mock_supabase_client):
        """Testa busca de leads quando não há dados"""
        # Arrange
        mock_response = Mock()
        mock_response.data = []

        mock_table = Mock()
        mock_table.select.return_value.range.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_all_leads()

        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_get_all_leads_pagination(self, service, mock_supabase_client, sample_lead_data):
        """Testa paginação de leads"""
        # Arrange
        # Primeira página com 1000 leads
        first_page = [sample_lead_data] * 1000
        # Segunda página com 500 leads
        second_page = [sample_lead_data] * 500

        mock_responses = [Mock(data=first_page), Mock(data=second_page)]

        mock_table = Mock()
        mock_table.select.return_value.range.return_value.execute.side_effect = mock_responses
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_all_leads()

        # Assert
        assert len(result) == 1500

    @pytest.mark.asyncio
    async def test_get_subscribed_leads_with_column(self, service, mock_supabase_client, sample_leads_list):
        """Testa busca de leads inscritos quando coluna subscribed existe"""
        # Arrange
        # Mock para verificação da coluna
        check_response = Mock(data=[{"subscribed": True}])
        # Mock para dados dos leads
        data_response = Mock(data=sample_leads_list)

        mock_table = Mock()
        mock_table.select.return_value.limit.return_value.execute.return_value = check_response
        mock_table.select.return_value.eq.return_value.range.return_value.execute.return_value = data_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_subscribed_leads()

        # Assert
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_create_lead_success(self, service, mock_supabase_client, sample_lead_data):
        """Testa criação de lead com sucesso"""
        # Arrange
        lead = LeadCreate(email="novo@exemplo.com", nome="Novo Lead")
        mock_response = Mock(data=[sample_lead_data])

        mock_table = Mock()
        mock_table.insert.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.create_lead(lead)

        # Assert
        assert result["email"] == "teste@exemplo.com"
        mock_table.insert.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_lead_without_name(self, service, mock_supabase_client, sample_lead_data):
        """Testa criação de lead sem nome"""
        # Arrange
        lead = LeadCreate(email="novo@exemplo.com", nome=None)
        mock_response = Mock(data=[sample_lead_data])

        mock_table = Mock()
        mock_table.insert.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.create_lead(lead)

        # Assert
        assert result is not None
        # Verifica que o insert foi chamado com nombre vazio
        call_args = mock_table.insert.call_args[0][0]
        assert call_args["nombre"] == ""

    @pytest.mark.asyncio
    async def test_create_lead_failure(self, service, mock_supabase_client):
        """Testa falha na criação de lead"""
        # Arrange
        lead = LeadCreate(email="novo@exemplo.com", nome="Novo Lead")
        mock_response = Mock(data=None)

        mock_table = Mock()
        mock_table.insert.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act & Assert
        with pytest.raises(Exception, match="Erro ao criar lead"):
            await service.create_lead(lead)

    @pytest.mark.asyncio
    async def test_delete_lead_success(self, service, mock_supabase_client, sample_lead_data):
        """Testa deleção de lead com sucesso"""
        # Arrange
        lead_id = "123e4567-e89b-12d3-a456-426614174000"
        mock_response = Mock(data=[sample_lead_data])

        mock_table = Mock()
        mock_table.delete.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.delete_lead(lead_id)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_lead_not_found(self, service, mock_supabase_client):
        """Testa deleção de lead não encontrado"""
        # Arrange
        lead_id = "999e4567-e89b-12d3-a456-426614174999"
        mock_response = Mock(data=[])

        mock_table = Mock()
        mock_table.delete.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.delete_lead(lead_id)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_unsubscribe_by_email_success(self, service, mock_supabase_client, sample_lead_data):
        """Testa cancelamento de inscrição por email com sucesso"""
        # Arrange
        email = "teste@exemplo.com"
        mock_response = Mock(data=[sample_lead_data])

        mock_table = Mock()
        mock_table.delete.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.unsubscribe_by_email(email)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_unsubscribe_by_email_not_found(self, service, mock_supabase_client):
        """Testa cancelamento de inscrição com email não encontrado"""
        # Arrange
        email = "naoexiste@exemplo.com"
        mock_response = Mock(data=[])

        mock_table = Mock()
        mock_table.delete.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.unsubscribe_by_email(email)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_get_lead_by_email_found(self, service, mock_supabase_client, sample_lead_data):
        """Testa busca de lead por email encontrado"""
        # Arrange
        email = "teste@exemplo.com"
        mock_response = Mock(data=[sample_lead_data])

        mock_table = Mock()
        mock_table.select.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_lead_by_email(email)

        # Assert
        assert result is not None
        assert result["email"] == "teste@exemplo.com"

    @pytest.mark.asyncio
    async def test_get_lead_by_email_not_found(self, service, mock_supabase_client):
        """Testa busca de lead por email não encontrado"""
        # Arrange
        email = "naoexiste@exemplo.com"
        mock_response = Mock(data=[])

        mock_table = Mock()
        mock_table.select.return_value.eq.return_value.execute.return_value = mock_response
        mock_supabase_client.table.return_value = mock_table

        # Act
        result = await service.get_lead_by_email(email)

        # Assert
        assert result is None
