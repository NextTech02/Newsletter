"""
Serviço de gerenciamento de usuários
"""

from typing import List, Dict, Optional
from supabase import create_client, Client
from app.config import settings
from app.models.auth_schemas import UserCreate, UserUpdate
from app.services.auth_service import get_password_hash, verify_password


class UserService:
    """Serviço para gerenciar operações com usuários"""

    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.table_name = settings.USERS_TABLE

    async def get_all_users(self) -> List[Dict]:
        """Busca todos os usuários (sem password_hash)"""
        response = self.client.table(self.table_name).select(
            "id, username, email, full_name, active, is_admin, created_at, updated_at"
        ).execute()

        return response.data if response.data else []

    async def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Busca um usuário pelo username (com password_hash para autenticação)"""
        response = self.client.table(self.table_name).select("*").eq(
            "username", username
        ).execute()

        if response.data:
            return response.data[0]
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Busca um usuário pelo ID"""
        response = self.client.table(self.table_name).select(
            "id, username, email, full_name, active, is_admin, created_at, updated_at"
        ).eq("id", user_id).execute()

        if response.data:
            return response.data[0]
        return None

    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Busca um usuário pelo email"""
        response = self.client.table(self.table_name).select(
            "id, username, email, full_name, active, is_admin, created_at, updated_at"
        ).eq("email", email).execute()

        if response.data:
            return response.data[0]
        return None

    async def create_user(self, user: UserCreate) -> Dict:
        """Cria um novo usuário"""
        # Verificar se username já existe
        existing = await self.get_user_by_username(user.username)
        if existing:
            raise ValueError("Username já existe")

        # Verificar se email já existe
        existing_email = await self.get_user_by_email(user.email)
        if existing_email:
            raise ValueError("Email já existe")

        # Hash da senha
        password_hash = get_password_hash(user.password)

        # Criar usuário
        data = {
            "username": user.username,
            "email": user.email,
            "password_hash": password_hash,
            "full_name": user.full_name,
            "active": True,
            "is_admin": user.is_admin
        }

        response = self.client.table(self.table_name).insert(data).execute()

        if response.data:
            # Retornar sem password_hash
            user_data = response.data[0]
            user_data.pop('password_hash', None)
            return user_data
        else:
            raise Exception("Erro ao criar usuário")

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Dict:
        """Atualiza um usuário"""
        data = {}

        if user_update.email is not None:
            # Verificar se email já existe em outro usuário
            existing = await self.get_user_by_email(user_update.email)
            if existing and existing['id'] != user_id:
                raise ValueError("Email já existe")
            data["email"] = user_update.email

        if user_update.full_name is not None:
            data["full_name"] = user_update.full_name

        if user_update.active is not None:
            data["active"] = user_update.active

        if user_update.is_admin is not None:
            data["is_admin"] = user_update.is_admin

        if user_update.password is not None:
            data["password_hash"] = get_password_hash(user_update.password)

        if not data:
            raise ValueError("Nenhum campo para atualizar")

        response = self.client.table(self.table_name).update(data).eq(
            "id", user_id
        ).execute()

        if response.data:
            user_data = response.data[0]
            user_data.pop('password_hash', None)
            return user_data
        else:
            raise Exception("Erro ao atualizar usuário")

    async def delete_user(self, user_id: str) -> bool:
        """Deleta um usuário"""
        response = self.client.table(self.table_name).delete().eq("id", user_id).execute()
        return bool(response.data)

    async def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Autentica um usuário

        Returns:
            User data (sem password_hash) se autenticado, None caso contrário
        """
        user = await self.get_user_by_username(username)

        if not user:
            return None

        if not verify_password(password, user.get('password_hash', '')):
            return None

        if not user.get('active', False):
            return None

        # Remover password_hash antes de retornar
        user.pop('password_hash', None)
        return user


# Instância global do serviço
user_service = UserService()
