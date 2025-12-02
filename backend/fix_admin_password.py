"""
Script para atualizar a senha do usuário admin
"""

import asyncio
from app.services.user_service import user_service
from app.services.auth_service import get_password_hash


async def fix_admin_password():
    """Atualiza a senha do usuário admin"""

    # Gerar novo hash
    new_hash = get_password_hash("admin123")
    print(f"Novo hash gerado: {new_hash[:50]}...")

    # Atualizar diretamente no Supabase
    try:
        response = user_service.client.table(user_service.table_name).update({
            "password_hash": new_hash
        }).eq("username", "admin").execute()

        if response.data:
            print("[SUCESSO] Senha do usuario admin atualizada!")
            print("Credenciais: username=admin, password=admin123")
        else:
            print("[ERRO] Nao foi possivel atualizar a senha")

    except Exception as e:
        print(f"[ERRO] {e}")


if __name__ == "__main__":
    asyncio.run(fix_admin_password())
