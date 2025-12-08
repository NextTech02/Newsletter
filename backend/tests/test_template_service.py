"""
Testes unitários para Template Service
"""

import pytest
from unittest.mock import patch
from app.services.template_service import generate_newsletter_html
from app.models.schemas import NewsItem


class TestTemplateService:
    """Testes para o serviço de templates"""

    def test_generate_newsletter_html_single_news(self):
        """Testa geração de HTML com uma única notícia"""
        # Arrange
        subject = "Newsletter Teste"
        news_items = [
            NewsItem(title="Notícia 1", content="Conteúdo da notícia 1")
        ]

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items)

            # Assert
            assert "Newsletter Teste" in html
            assert "Notícia 1" in html
            assert "Conteúdo da notícia 1" in html
            assert "<!DOCTYPE html>" in html
            assert "Federación Colombiana de Póker" in html

    def test_generate_newsletter_html_multiple_news(self):
        """Testa geração de HTML com múltiplas notícias"""
        # Arrange
        subject = "Newsletter Semanal"
        news_items = [
            NewsItem(title="Notícia 1", content="Conteúdo 1"),
            NewsItem(title="Notícia 2", content="Conteúdo 2"),
            NewsItem(title="Notícia 3", content="Conteúdo 3")
        ]

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items)

            # Assert
            assert "Notícia 1" in html
            assert "Notícia 2" in html
            assert "Notícia 3" in html
            assert "Conteúdo 1" in html
            assert "Conteúdo 2" in html
            assert "Conteúdo 3" in html
            # Verifica numeração
            assert "1. Notícia 1" in html
            assert "2. Notícia 2" in html
            assert "3. Notícia 3" in html

    def test_generate_newsletter_html_with_theme(self):
        """Testa geração de HTML com tema específico"""
        # Arrange
        subject = "Newsletter"
        news_items = [NewsItem(title="Teste", content="Conteúdo")]
        theme = "federacion_poker"

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items, theme)

            # Assert
            assert "#00a6bc" in html  # Cor primária do tema
            assert "#32373c" in html  # Cor terciária do tema

    def test_generate_newsletter_html_unsubscribe_link(self):
        """Testa se o link de cancelamento de inscrição está presente"""
        # Arrange
        subject = "Newsletter"
        news_items = [NewsItem(title="Teste", content="Conteúdo")]

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items)

            # Assert
            assert "http://localhost:3000/unsubscribe" in html
            assert "Cancelar inscrição" in html
            assert "Cancelar suscripción" in html

    def test_generate_newsletter_html_special_characters(self):
        """Testa geração com caracteres especiais"""
        # Arrange
        subject = "Newsletter com Ñ e Ç"
        news_items = [
            NewsItem(
                title="Título com àçãõ",
                content="Conteúdo com ñ, ü e outros: <>&"
            )
        ]

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items)

            # Assert
            assert "Newsletter com Ñ e Ç" in html
            assert "Título com àçãõ" in html
            assert "Conteúdo com ñ, ü e outros: <>&" in html

    def test_generate_newsletter_html_structure(self):
        """Testa estrutura básica do HTML"""
        # Arrange
        subject = "Newsletter"
        news_items = [NewsItem(title="Teste", content="Conteúdo")]

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items)

            # Assert
            # Verifica tags essenciais
            assert "<!DOCTYPE html>" in html
            assert "<html lang=\"pt-BR\">" in html
            assert "<head>" in html
            assert "<body" in html
            assert "</body>" in html
            assert "</html>" in html
            # Verifica meta tags
            assert '<meta charset="UTF-8">' in html
            assert '<meta name="viewport"' in html

    def test_generate_newsletter_html_footer(self):
        """Testa se o rodapé está presente"""
        # Arrange
        subject = "Newsletter"
        news_items = [NewsItem(title="Teste", content="Conteúdo")]

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items)

            # Assert
            assert "© 2024 Federación Colombiana de Póker" in html

    def test_generate_newsletter_html_header(self):
        """Testa se o cabeçalho está presente"""
        # Arrange
        subject = "Newsletter Especial"
        news_items = [NewsItem(title="Teste", content="Conteúdo")]

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items)

            # Assert
            assert "Newsletter Especial" in html
            assert "Federación Colombiana de Póker" in html
            assert "Póquer - Un deporte mental" in html

    def test_generate_newsletter_html_empty_news_list(self):
        """Testa geração com lista de notícias vazia"""
        # Arrange
        subject = "Newsletter Vazia"
        news_items = []

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items)

            # Assert
            assert "Newsletter Vazia" in html
            assert "<!DOCTYPE html>" in html
            # Não deve haver div de notícias
            assert html.count('<div style="margin-bottom: 30px') == 0

    def test_generate_newsletter_html_long_content(self):
        """Testa geração com conteúdo longo"""
        # Arrange
        subject = "Newsletter Longa"
        long_content = "Lorem ipsum " * 100
        news_items = [NewsItem(title="Notícia Longa", content=long_content)]

        with patch('app.services.template_service.settings') as mock_settings:
            mock_settings.FRONTEND_URL = "http://localhost:3000"

            # Act
            html = generate_newsletter_html(subject, news_items)

            # Assert
            assert long_content in html
            assert "Notícia Longa" in html
