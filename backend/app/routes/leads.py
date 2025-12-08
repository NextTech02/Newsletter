"""
Rotas para gerenciamento de Leads
"""

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    Lead, LeadCreate, LeadsList, MessageResponse, UnsubscribeRequest
)
from app.services.supabase_service import supabase_service

router = APIRouter()


@router.get("/", response_model=LeadsList)
async def get_all_leads():
    """Retorna todos os leads"""
    try:
        leads = await supabase_service.get_all_leads()
        return {"total": len(leads), "leads": leads}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar leads: {str(e)}"
        )


@router.get("/subscribed", response_model=LeadsList)
async def get_subscribed_leads():
    """Retorna apenas leads inscritos"""
    try:
        leads = await supabase_service.get_subscribed_leads()
        return {"total": len(leads), "leads": leads}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar leads inscritos: {str(e)}"
        )


@router.post("/", response_model=Lead, status_code=status.HTTP_201_CREATED)
async def create_lead(lead: LeadCreate):
    """Cria um novo lead"""
    try:
        # Verificar se já existe
        existing = await supabase_service.get_lead_by_email(lead.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

        new_lead = await supabase_service.create_lead(lead)
        return new_lead
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar lead: {str(e)}"
        )


@router.delete("/{lead_id}", response_model=MessageResponse)
async def delete_lead(lead_id: str):
    """Deleta um lead pelo ID"""
    try:
        success = await supabase_service.delete_lead(lead_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead não encontrado"
            )
        return {"message": "Lead removido com sucesso", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar lead: {str(e)}"
        )


@router.post("/unsubscribe", response_model=MessageResponse)
async def unsubscribe(request: UnsubscribeRequest):
    """
    Cancela inscrição de um lead pelo email

    Recebe:
    - email: Email do lead a ser removido
    - reason: Motivo do cancelamento
    - comments: Comentários adicionais (opcional)
    """
    try:
        # Verificar se o email existe antes de deletar
        existing_lead = await supabase_service.get_lead_by_email(request.email)
        if not existing_lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email não encontrado na lista de inscritos"
            )

        # Deletar o lead
        success = await supabase_service.unsubscribe_by_email(request.email)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar cancelamento"
            )

        # Log do motivo e comentários (pode ser usado para análise futura)
        print(f"[UNSUBSCRIBE] Email: {request.email}, Motivo: {request.reason}, Comentários: {request.comments or 'Nenhum'}")

        return {"message": "Inscrição cancelada com sucesso", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cancelar inscrição: {str(e)}"
        )
