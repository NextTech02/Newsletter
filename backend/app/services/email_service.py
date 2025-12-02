"""
Serviço de envio de emails
"""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from typing import List, Tuple, Optional
import asyncio


class EmailService:
    """Serviço para envio de emails via SMTP"""

    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD

    async def send_email(
        self,
        recipient: str,
        subject: str,
        html_content: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Envia um email para um destinatário

        Returns:
            Tuple[success, error_message]
        """
        try:
            message = MIMEMultipart("alternative")
            message["From"] = self.smtp_username
            message["To"] = recipient
            message["Subject"] = subject

            # Anexar conteúdo HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Enviar email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_server,
                port=self.smtp_port,
                start_tls=True,
                username=self.smtp_username,
                password=self.smtp_password,
            )

            return True, None

        except Exception as e:
            return False, str(e)

    async def send_bulk_emails(
        self,
        recipients: List[str],
        subject: str,
        html_content: str,
        batch_size: int = 50
    ) -> Tuple[int, int, List[str]]:
        """
        Envia emails em lote com controle de taxa

        Returns:
            Tuple[total_sent, total_failed, error_messages]
        """
        total_sent = 0
        total_failed = 0
        errors = []

        # Processar em lotes
        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i + batch_size]

            # Enviar batch de forma assíncrona
            tasks = [
                self.send_email(recipient, subject, html_content)
                for recipient in batch
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Contar resultados
            for recipient, result in zip(batch, results):
                if isinstance(result, Exception):
                    total_failed += 1
                    errors.append(f"{recipient}: {str(result)}")
                else:
                    success, error = result
                    if success:
                        total_sent += 1
                    else:
                        total_failed += 1
                        errors.append(f"{recipient}: {error}")

            # Pequena pausa entre lotes para evitar sobrecarga
            if i + batch_size < len(recipients):
                await asyncio.sleep(1)

        return total_sent, total_failed, errors


# Instância global do serviço
email_service = EmailService()
