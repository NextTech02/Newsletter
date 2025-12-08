"""
Testes unitários para EmailService
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.email_service import EmailService


class TestEmailService:
    """Testes para o serviço de email"""

    @pytest.fixture
    def service(self):
        """Cria uma instância do serviço"""
        with patch('app.services.email_service.settings') as mock_settings:
            mock_settings.SMTP_SERVER = "smtp.test.com"
            mock_settings.SMTP_PORT = 587
            mock_settings.SMTP_USERNAME = "test@test.com"
            mock_settings.SMTP_PASSWORD = "test_password"
            return EmailService()

    @pytest.mark.asyncio
    async def test_send_email_success(self, service):
        """Testa envio de email com sucesso"""
        # Arrange
        recipient = "destinatario@exemplo.com"
        subject = "Assunto Teste"
        html_content = "<h1>Conteúdo HTML</h1>"

        with patch('app.services.email_service.aiosmtplib.send', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = None

            # Act
            success, error = await service.send_email(recipient, subject, html_content)

            # Assert
            assert success is True
            assert error is None
            mock_send.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_email_failure(self, service):
        """Testa falha no envio de email"""
        # Arrange
        recipient = "destinatario@exemplo.com"
        subject = "Assunto Teste"
        html_content = "<h1>Conteúdo HTML</h1>"

        with patch('app.services.email_service.aiosmtplib.send', new_callable=AsyncMock) as mock_send:
            mock_send.side_effect = Exception("Erro de conexão SMTP")

            # Act
            success, error = await service.send_email(recipient, subject, html_content)

            # Assert
            assert success is False
            assert "Erro de conexão SMTP" in error

    @pytest.mark.asyncio
    async def test_send_bulk_emails_all_success(self, service):
        """Testa envio em massa com todos os emails bem-sucedidos"""
        # Arrange
        recipients = ["user1@test.com", "user2@test.com", "user3@test.com"]
        subject = "Newsletter Teste"
        html_content = "<h1>Newsletter</h1>"

        with patch.object(service, 'send_email', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = (True, None)

            # Act
            sent, failed, errors = await service.send_bulk_emails(
                recipients, subject, html_content, batch_size=2
            )

            # Assert
            assert sent == 3
            assert failed == 0
            assert len(errors) == 0
            assert mock_send.call_count == 3

    @pytest.mark.asyncio
    async def test_send_bulk_emails_partial_failure(self, service):
        """Testa envio em massa com algumas falhas"""
        # Arrange
        recipients = ["user1@test.com", "user2@test.com", "user3@test.com"]
        subject = "Newsletter Teste"
        html_content = "<h1>Newsletter</h1>"

        with patch.object(service, 'send_email', new_callable=AsyncMock) as mock_send:
            # Primeiro sucesso, segundo falha, terceiro sucesso
            mock_send.side_effect = [
                (True, None),
                (False, "Erro no envio"),
                (True, None)
            ]

            # Act
            sent, failed, errors = await service.send_bulk_emails(
                recipients, subject, html_content
            )

            # Assert
            assert sent == 2
            assert failed == 1
            assert len(errors) == 1
            assert "user2@test.com" in errors[0]

    @pytest.mark.asyncio
    async def test_send_bulk_emails_all_failure(self, service):
        """Testa envio em massa com todas as falhas"""
        # Arrange
        recipients = ["user1@test.com", "user2@test.com"]
        subject = "Newsletter Teste"
        html_content = "<h1>Newsletter</h1>"

        with patch.object(service, 'send_email', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = (False, "Falha no servidor SMTP")

            # Act
            sent, failed, errors = await service.send_bulk_emails(
                recipients, subject, html_content
            )

            # Assert
            assert sent == 0
            assert failed == 2
            assert len(errors) == 2

    @pytest.mark.asyncio
    async def test_send_bulk_emails_with_exception(self, service):
        """Testa envio em massa com exceção durante processamento"""
        # Arrange
        recipients = ["user1@test.com", "user2@test.com"]
        subject = "Newsletter Teste"
        html_content = "<h1>Newsletter</h1>"

        with patch.object(service, 'send_email', new_callable=AsyncMock) as mock_send:
            mock_send.side_effect = [
                (True, None),
                Exception("Erro crítico")
            ]

            # Act
            sent, failed, errors = await service.send_bulk_emails(
                recipients, subject, html_content
            )

            # Assert
            assert sent == 1
            assert failed == 1
            assert len(errors) == 1
            assert "Erro crítico" in errors[0]

    @pytest.mark.asyncio
    async def test_send_bulk_emails_empty_list(self, service):
        """Testa envio em massa com lista vazia"""
        # Arrange
        recipients = []
        subject = "Newsletter Teste"
        html_content = "<h1>Newsletter</h1>"

        # Act
        sent, failed, errors = await service.send_bulk_emails(
            recipients, subject, html_content
        )

        # Assert
        assert sent == 0
        assert failed == 0
        assert len(errors) == 0

    @pytest.mark.asyncio
    async def test_send_bulk_emails_batch_processing(self, service):
        """Testa processamento em lotes"""
        # Arrange
        # 5 destinatários com batch_size=2 deve criar 3 lotes (2, 2, 1)
        recipients = [f"user{i}@test.com" for i in range(5)]
        subject = "Newsletter Teste"
        html_content = "<h1>Newsletter</h1>"

        with patch.object(service, 'send_email', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = (True, None)

            with patch('app.services.email_service.asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                # Act
                sent, failed, errors = await service.send_bulk_emails(
                    recipients, subject, html_content, batch_size=2
                )

                # Assert
                assert sent == 5
                assert failed == 0
                # Deve haver 2 pausas (entre os 3 lotes)
                assert mock_sleep.call_count == 2
