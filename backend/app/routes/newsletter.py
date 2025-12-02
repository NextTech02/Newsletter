"""
Rotas para Newsletter
"""

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    NewsletterCreate, NewsletterPreview,
    EmailSendRequest, EmailSendResponse
)
from app.services.supabase_service import supabase_service
from app.services.email_service import email_service
from app.services.template_service import generate_newsletter_html

router = APIRouter()


@router.post("/preview", response_model=NewsletterPreview)
async def preview_newsletter(newsletter: NewsletterCreate):
    """Gera preview HTML da newsletter"""
    try:
        html = generate_newsletter_html(
            subject=newsletter.subject,
            news_items=newsletter.news_items,
            theme=newsletter.theme
        )
        return {"html": html}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar preview: {str(e)}"
        )


@router.post("/send", response_model=EmailSendResponse)
async def send_newsletter(email_request: EmailSendRequest):
    """Envia newsletter por email"""
    try:
        # Determinar destinatários
        if email_request.recipients:
            recipients = email_request.recipients
        else:
            # Buscar todos os leads inscritos
            leads = await supabase_service.get_subscribed_leads()
            recipients = [lead["email"] for lead in leads]

        if not recipients:
            return EmailSendResponse(
                success=False,
                total_sent=0,
                total_failed=0,
                message="Nenhum destinatário encontrado"
            )

        # Enviar emails
        if email_request.is_test:
            # Enviar apenas para o remetente como teste
            success, error = await email_service.send_email(
                recipient=email_service.smtp_username,
                subject=f"[TESTE] {email_request.subject}",
                html_content=email_request.html_content
            )

            if success:
                return EmailSendResponse(
                    success=True,
                    total_sent=1,
                    total_failed=0,
                    message="Email de teste enviado com sucesso"
                )
            else:
                return EmailSendResponse(
                    success=False,
                    total_sent=0,
                    total_failed=1,
                    message="Erro ao enviar email de teste",
                    errors=[error]
                )
        else:
            # Enviar para todos
            total_sent, total_failed, errors = await email_service.send_bulk_emails(
                recipients=recipients,
                subject=email_request.subject,
                html_content=email_request.html_content
            )

            return EmailSendResponse(
                success=(total_sent > 0),
                total_sent=total_sent,
                total_failed=total_failed,
                message=f"Enviados: {total_sent}, Falhas: {total_failed}",
                errors=errors if errors else None
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao enviar newsletter: {str(e)}"
        )
