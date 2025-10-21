import streamlit as st
from supabase import create_client, Client
from config import get_supabase_config
import pandas as pd
from typing import List, Dict, Optional

class SupabaseManager:
    def __init__(self):
        self.supabase_url, self.supabase_key = get_supabase_config()
        self.client: Optional[Client] = None
        self.page_size = 1000  # Tamanho da página para paginação
        
    def connect(self) -> bool:
        """Conecta ao Supabase"""
        try:
            if not self.supabase_url or not self.supabase_key:
                return False
            
            self.client = create_client(self.supabase_url, self.supabase_key)
            return True
        except Exception as e:
            st.error(f"Erro ao conectar com Supabase: {str(e)}")
            return False
    
    def _paginated_query(self, query, table_name: str, show_progress: bool = True) -> List[Dict]:
        """Executa uma query com paginação para buscar todos os registros"""
        all_data = []
        offset = 0
        
        while True:
            try:
                response = query.range(offset, offset + self.page_size - 1).execute()
                
                if not response.data:
                    break
                
                all_data.extend(response.data)
                
                # Se retornou menos que o page_size, chegamos ao fim
                if len(response.data) < self.page_size:
                    break
                
                offset += self.page_size
                
            except Exception as e:
                st.error(f"Erro na paginação da tabela {table_name}: {str(e)}")
                break
        
        return all_data
    
    def get_leads(self, table_name: str = "newsletter_leads", show_progress: bool = True) -> List[Dict]:
        """Busca todos os leads da tabela com paginação"""
        if not self.client:
            if not self.connect():
                return []
        
        try:
            query = self.client.table(table_name).select("*")
            return self._paginated_query(query, table_name, show_progress)
        except Exception as e:
            st.error(f"Erro ao buscar leads: {str(e)}")
            return []
    
    def add_lead(self, email: str, name: str = "", table_name: str = "newsletter_leads") -> bool:
        """Adiciona um novo lead"""
        if not self.client:
            if not self.connect():
                return False
        
        try:
            # Criar dados apenas com as colunas que existem
            data = {
                "email": email
            }
            
            # Adicionar nome apenas se fornecido
            if name:
                data["nome"] = name
            
            response = self.client.table(table_name).insert(data).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao adicionar lead: {str(e)}")
            return False
    
    def update_lead(self, lead_id: int, data: Dict, table_name: str = "newsletter_leads") -> bool:
        """Atualiza um lead existente"""
        if not self.client:
            if not self.connect():
                return False
        
        try:
            response = self.client.table(table_name).update(data).eq("id", lead_id).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar lead: {str(e)}")
            return False
    
    def delete_lead(self, lead_id: int, table_name: str = "newsletter_leads") -> bool:
        """Remove um lead"""
        if not self.client:
            if not self.connect():
                return False
        
        try:
            response = self.client.table(table_name).delete().eq("id", lead_id).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao remover lead: {str(e)}")
            return False
    
    def get_subscribed_leads(self, table_name: str = "newsletter_leads", show_progress: bool = True) -> List[Dict]:
        """Busca apenas leads que estão inscritos com paginação"""
        if not self.client:
            if not self.connect():
                return []
        
        try:
            # Primeiro, verificar se a coluna 'subscribed' existe
            response = self.client.table(table_name).select("*").limit(1).execute()
            if response.data and 'subscribed' in response.data[0]:
                # Se a coluna existe, filtrar por subscribed = True com paginação
                query = self.client.table(table_name).select("*").eq("subscribed", True)
                return self._paginated_query(query, table_name, show_progress)
            else:
                # Se a coluna não existe, retornar todos os leads (considerando todos como inscritos) com paginação
                query = self.client.table(table_name).select("*")
                return self._paginated_query(query, table_name, show_progress)
        except Exception as e:
            st.error(f"Erro ao buscar leads inscritos: {str(e)}")
            return []
    
    def get_leads_dataframe(self, table_name: str = "newsletter_leads") -> pd.DataFrame:
        """Retorna os leads como DataFrame do pandas com apenas email e nome"""
        leads = self.get_leads(table_name, show_progress=False)
        
        if not leads:
            return pd.DataFrame(columns=['email', 'nome'])
        
        # Criar DataFrame apenas com email e nome
        df = pd.DataFrame(leads)
        
        # Selecionar apenas as colunas que existem
        columns_to_keep = []
        if 'email' in df.columns:
            columns_to_keep.append('email')
        if 'nome' in df.columns:
            columns_to_keep.append('nome')
        
        if columns_to_keep:
            df = df[columns_to_keep]
        else:
            # Se não encontrar as colunas esperadas, mostrar todas
            df = df
        
        return df
    
    def unsubscribe_by_email(self, email: str, table_name: str = "newsletter_leads") -> bool:
        """Remove um lead pelo email (cancelar inscrição)"""
        if not self.client:
            if not self.connect():
                return False
        
        try:
            response = self.client.table(table_name).delete().eq("email", email).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao cancelar inscrição: {str(e)}")
            return False
    
    def process_unsubscribe(self, email: str, table_name: str = "newsletter_leads") -> dict:
        """Processa cancelamento de inscrição com validação e logging"""
        try:
            # Validar email
            if not email or '@' not in email:
                return {
                    'success': False,
                    'message': 'Email inválido',
                    'email': email
                }
            
            # Verificar se o email existe
            existing = self.client.table(table_name).select('email').eq('email', email).execute()
            
            if not existing.data:
                return {
                    'success': False,
                    'message': 'Email não encontrado na base de dados',
                    'email': email
                }
            
            # Remover o email
            result = self.client.table(table_name).delete().eq('email', email).execute()
            
            if result.data:
                # Limpar cache
                self.clear_cache()
                return {
                    'success': True,
                    'message': 'Inscrição cancelada com sucesso',
                    'email': email,
                    'removed_count': len(result.data)
                }
            else:
                return {
                    'success': False,
                    'message': 'Erro ao remover email do banco de dados',
                    'email': email
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro interno: {str(e)}',
                'email': email
            }
    
    def clear_cache(self):
        """Limpa o cache de leads"""
        if hasattr(self, '_cached_leads'):
            self._cached_leads = None
