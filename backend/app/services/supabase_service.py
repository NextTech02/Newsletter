"""
Serviço de integração com Supabase
"""

from supabase import create_client, Client
from app.config import settings
from typing import List, Dict, Optional
from app.models.schemas import Lead, LeadCreate


class SupabaseService:
    """Serviço para gerenciar operações com Supabase"""

    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.table_name = settings.LEADS_TABLE
        self.page_size = 1000

    async def get_all_leads(self) -> List[Dict]:
        """Busca todos os leads com paginação"""
        all_data = []
        offset = 0

        while True:
            response = self.client.table(self.table_name).select("*").range(
                offset, offset + self.page_size - 1
            ).execute()

            if not response.data:
                break

            all_data.extend(response.data)

            if len(response.data) < self.page_size:
                break

            offset += self.page_size

        return all_data

    async def get_subscribed_leads(self) -> List[Dict]:
        """Busca apenas leads inscritos"""
        # Primeiro verifica se a coluna 'subscribed' existe
        response = self.client.table(self.table_name).select("*").limit(1).execute()

        if response.data and 'subscribed' in response.data[0]:
            # Filtra por subscribed = True
            all_data = []
            offset = 0

            while True:
                response = self.client.table(self.table_name).select("*").eq(
                    "subscribed", True
                ).range(offset, offset + self.page_size - 1).execute()

                if not response.data:
                    break

                all_data.extend(response.data)

                if len(response.data) < self.page_size:
                    break

                offset += self.page_size

            return all_data
        else:
            # Se a coluna não existe, retorna todos
            return await self.get_all_leads()

    async def create_lead(self, lead: LeadCreate) -> Dict:
        """Cria um novo lead"""
        data = {"email": lead.email}

        if lead.nome:
            data["nome"] = lead.nome

        response = self.client.table(self.table_name).insert(data).execute()

        if response.data:
            return response.data[0]
        else:
            raise Exception("Erro ao criar lead")

    async def delete_lead(self, lead_id: str) -> bool:
        """Deleta um lead"""
        response = self.client.table(self.table_name).delete().eq("id", lead_id).execute()
        return bool(response.data)

    async def unsubscribe_by_email(self, email: str) -> bool:
        """Cancela inscrição de um lead pelo email"""
        response = self.client.table(self.table_name).delete().eq("email", email).execute()
        return bool(response.data)

    async def get_lead_by_email(self, email: str) -> Optional[Dict]:
        """Busca um lead pelo email"""
        response = self.client.table(self.table_name).select("*").eq("email", email).execute()

        if response.data:
            return response.data[0]
        return None


# Instância global do serviço
supabase_service = SupabaseService()
