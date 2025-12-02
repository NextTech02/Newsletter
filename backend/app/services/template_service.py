"""
Serviço de geração de templates HTML
"""

from typing import List
from app.models.schemas import NewsItem
from app.config import settings


def generate_newsletter_html(
    subject: str,
    news_items: List[NewsItem],
    theme: str = "federacion_poker"
) -> str:
    """
    Gera HTML da newsletter

    Args:
        subject: Assunto da newsletter
        news_items: Lista de notícias
        theme: Tema visual (padrão: federacion_poker)

    Returns:
        HTML completo da newsletter
    """

    # Cores do tema FCP (Federación Colombiana de Póker)
    colors = {
        "primary": "#00a6bc",      # Cyan/Teal principal
        "secondary": "#75cede",    # Cyan claro
        "tertiary": "#32373c",     # Cinza escuro
        "background": "#f5f5f5",
        "text": "#000000"
    }

    # Gerar HTML das notícias
    news_html = ""
    for i, news in enumerate(news_items, 1):
        news_html += f"""
        <div style="margin-bottom: 30px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h2 style="color: {colors['primary']}; margin-top: 0; font-size: 20px; font-weight: 600;">
                {i}. {news.title}
            </h2>
            <p style="color: {colors['text']}; line-height: 1.6; margin: 0; font-size: 15px;">
                {news.content}
            </p>
        </div>
        """

    # Template completo
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: {colors['background']}; font-family: 'Arial', sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">

            <!-- Header -->
            <div style="background: linear-gradient(135deg, {colors['tertiary']} 0%, {colors['primary']} 50%, {colors['secondary']} 100%); padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px; font-weight: bold;">
                    {subject}
                </h1>
                <p style="color: white; margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">
                    Federación Colombiana de Póker
                </p>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 12px; font-style: italic;">
                    Póquer - Un deporte mental
                </p>
            </div>

            <!-- Content -->
            <div style="background: white; padding: 30px; border-radius: 0 0 8px 8px;">
                {news_html}
            </div>

            <!-- Footer -->
            <div style="text-align: center; padding: 20px; color: #666; font-size: 12px;">
                <p style="margin: 0 0 10px 0;">© 2024 Federación Colombiana de Póker</p>
                <p style="margin: 0;">
                    <a href="{settings.FRONTEND_URL}/unsubscribe" style="color: {colors['primary']}; text-decoration: none;">
                        Cancelar inscrição / Cancelar suscripción
                    </a>
                </p>
            </div>

        </div>
    </body>
    </html>
    """

    return html
