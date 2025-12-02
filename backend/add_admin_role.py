"""
Script para adicionar coluna is_admin e atualizar o usuário admin
Execute: python add_admin_role.py
"""

import asyncio
from app.services.user_service import user_service


async def add_admin_role():
    """Adiciona coluna is_admin e atualiza o usuário admin"""

    try:
        # Verificar se a coluna já existe consultando um usuário
        response = user_service.client.table(user_service.table_name).select("*").limit(1).execute()

        if response.data and 'is_admin' in response.data[0]:
            print("[INFO] Coluna 'is_admin' ja existe")
        else:
            print("[INFO] Adicionando coluna 'is_admin' a tabela...")
            # Nota: Esta operação deve ser feita pelo administrador do banco diretamente
            # pois o cliente Supabase não suporta ALTER TABLE
            print("[ACAO NECESSARIA] Execute este SQL no Supabase:")
            print("ALTER TABLE users_newsletter ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE;")
            print("\nApos executar o SQL acima, execute este script novamente.\n")
            return

        # Atualizar o usuário admin para is_admin = True
        print("[INFO] Atualizando usuario 'admin' para is_admin=true...")
        response = user_service.client.table(user_service.table_name).update({
            "is_admin": True
        }).eq("username", "admin").execute()

        if response.data:
            print("[SUCESSO] Usuario 'admin' atualizado com permissoes de administrador!")
        else:
            print("[ERRO] Nao foi possivel atualizar o usuario admin")
            print("[INFO] Certifique-se de que o usuario 'admin' existe")

    except Exception as e:
        print(f"[ERRO] {e}")


if __name__ == "__main__":
    asyncio.run(add_admin_role())
