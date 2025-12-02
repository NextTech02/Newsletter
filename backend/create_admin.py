"""
Script para criar o primeiro usuário administrador
Execute: python create_admin.py
"""

import asyncio
from app.services.user_service import user_service
from app.models.auth_schemas import UserCreate


async def create_admin_user():
    """Cria o usuário administrador padrão"""

    admin_data = UserCreate(
        username="admin",
        email="admin@fcp.com",
        password="admin123",  # ALTERE esta senha após o primeiro login!
        full_name="Administrador FCP",
        is_admin=True
    )

    try:
        # Verificar se já existe
        existing = await user_service.get_user_by_username("admin")
        if existing:
            print("[ERRO] Usuario 'admin' ja existe!")
            print(f"   Email: {existing.get('email')}")
            print(f"   Criado em: {existing.get('created_at')}")
            return

        # Criar usuário
        user = await user_service.create_user(admin_data)
        print("[SUCESSO] Usuario administrador criado com sucesso!")
        print(f"   Username: {user['username']}")
        print(f"   Email: {user['email']}")
        print(f"   Senha: admin123")
        print("\n[IMPORTANTE] Altere a senha apos o primeiro login!")

    except Exception as e:
        print(f"[ERRO] Erro ao criar usuario: {e}")


if __name__ == "__main__":
    asyncio.run(create_admin_user())
