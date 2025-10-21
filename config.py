import os
import streamlit as st

def get_supabase_config():
    """Obtém configurações do Supabase"""
    # Tenta carregar do arquivo .env primeiro
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Configurações do Supabase
    supabase_url = os.getenv('SUPABASE_URL', '')
    supabase_key = os.getenv('SUPABASE_KEY', '')
    
    # Se não estiver nas variáveis de ambiente, usa os valores da sessão do Streamlit
    if not supabase_url:
        supabase_url = st.session_state.get('supabase_url', '')
    if not supabase_key:
        supabase_key = st.session_state.get('supabase_key', '')
    
    return supabase_url, supabase_key

def get_email_config():
    """Obtém configurações de email"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    return {
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'smtp_username': os.getenv('SMTP_USERNAME', ''),
        'smtp_password': os.getenv('SMTP_PASSWORD', '')
    }
