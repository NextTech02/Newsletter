import streamlit as st
from st_login_form import login_form
import os

# Configurar a página
st.set_page_config(page_title="Login", page_icon="🔐")

# Inicializar estado de sessão se não existir
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Configurar o formulário de login - APENAS LOGIN (sem criar conta ou guest)
try:
    client = login_form(
        allow_guest=False,      # Desabilita login como convidado
        allow_create=False      # Desabilita criação de nova conta
    )
except Exception as e:
    st.error(f"Erro no login form: {e}")
    st.stop()

# Verificar status de autenticação
if st.session_state.get("authenticated", False):
    # Usuário autenticado - redirecionar para app principal
    username = st.session_state.get("username", "")
    
    st.success(f"✅ Autenticado como {username}!")
    st.info("🔄 Redirecionando para o aplicativo principal...")
    
    # Aguardar 1 segundo antes de redirecionar
    import time
    time.sleep(1)
    
    # Redirecionar para app.py (que está em pages/)
    st.switch_page("pages/Newsletter.py")
    
