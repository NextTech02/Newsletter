import streamlit as st
import datetime
from typing import List, Dict
import pandas as pd
import base64
import os
import time
from supabase_manager import SupabaseManager
from email_manager import EmailManager
from config import get_supabase_config, get_email_config

# ============================================
# VERIFICAÇÃO DE AUTENTICAÇÃO
# ============================================
# Verificar se o usuário está autenticado
if not st.session_state.get("authenticated", False):
    st.warning("Você precisa fazer login primeiro!")
    st.info("🔄 Redirecionando para a página de login...")
    time.sleep(1)
    st.switch_page("login.py")
    st.stop()

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Newsletter FCP",
    page_icon="📰",
    layout="wide"
)

supabase_manager = SupabaseManager()
email_manager = EmailManager()

# ============================================
# INICIALIZAR ESTADO DA SESSÃO
# ============================================
if 'newsletter_title' not in st.session_state:
    st.session_state.newsletter_title = ""
if 'news_items' not in st.session_state:
    st.session_state.news_items = [{"title": "", "content": ""}]
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = "Federación Poker"
if 'site_dark_mode' not in st.session_state:
    st.session_state.site_dark_mode = False
if 'supabase_configured' not in st.session_state:
    st.session_state.supabase_configured = False
if 'leads_data' not in st.session_state:
    st.session_state.leads_data = []

# Sidebar com informações do usuário
with st.sidebar:
    # ============================================
    # SEÇÃO: USUÁRIO
    # ============================================
    st.markdown("### 👤 Usuário")
    username = st.session_state.get("username", "Usuário")
    st.info(f"**{username}**")
    
    # Botão de logout
    if st.button("Sair", use_container_width=True, type="secondary"):
        # Limpar sessão
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Logout realizado!")
        time.sleep(1)
        st.switch_page("login.py")
    
    st.markdown("---")
    
    # ============================================
    # SEÇÃO: NEWSLETTER
    # ============================================
    st.markdown("### Newsletter")
    
    # Data da newsletter
    newsletter_date = st.date_input(
        "Data",
        value=datetime.date.today(),
        help="Data que aparecerá na newsletter"
    )
    
    # Tema da newsletter
    theme = "Federación Poker"
    st.session_state.selected_theme = theme

    st.session_state.selected_theme = theme
    
    compact_mode = True
    layout_style = "Moderno"
    
    st.markdown("---")
    
    # ============================================
    # SEÇÃO: CONEXÕES
    # ============================================
    st.markdown("### Conexões")
    
    # Status Supabase
    supabase_url, supabase_key = get_supabase_config()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if supabase_url and supabase_key:
            st.success("✅ Supabase")
        else:
            st.error("❌ Supabase")
    with col2:
        if st.button("⚙️", key="config_supabase", help="Configurar Supabase"):
            st.session_state.show_supabase_config = not st.session_state.get("show_supabase_config", False)
    
    # Expandir configuração Supabase se necessário
    if st.session_state.get("show_supabase_config", False) or (not supabase_url or not supabase_key):
        with st.expander("Configurar Supabase", expanded=True):
            st.caption("Configure para gerenciar leads")
            url = st.text_input("URL", placeholder="https://seu-projeto.supabase.co", key="sb_url")
            key = st.text_input("Key", type="password", placeholder="sua-chave-aqui", key="sb_key")
            
            if st.button("Salvar", type="primary", use_container_width=True):
                if url and key:
                    st.session_state.supabase_url = url
                    st.session_state.supabase_key = key
                    st.session_state.show_supabase_config = False
                    st.success("✅ Salvo!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos")
    
    # Status Email
    email_config = get_email_config()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if email_config['smtp_username'] and email_config['smtp_password']:
            st.success("✅ Email")
        else:
            st.error("❌ Email")
    with col2:
        if st.button("⚙️", key="config_email", help="Configurar Email"):
            st.session_state.show_email_config = not st.session_state.get("show_email_config", False)
    
    # Expandir configuração Email se necessário
    if st.session_state.get("show_email_config", False) or (not email_config['smtp_username'] or not email_config['smtp_password']):
        with st.expander("Configurar Email", expanded=True):
            st.caption("Configure para enviar newsletters")
            st.warning("Use senha de aplicativo do Gmail, não sua senha normal!")
            
            username = st.text_input("Email", placeholder="seu@gmail.com", key="email_user")
            password = st.text_input("Senha de Aplicativo", type="password", placeholder="xxxx xxxx xxxx xxxx", key="email_pass")
            
            if st.button("Salvar", type="primary", use_container_width=True, key="save_email"):
                if username and password:
                    os.environ['SMTP_USERNAME'] = username
                    os.environ['SMTP_PASSWORD'] = password
                    st.session_state.show_email_config = False
                    st.success("✅ Salvo!")
                    st.rerun()
                else:
                    st.error("⚠️ Preencha todos os campos")
    
    st.markdown("---")
    
    # ============================================
    # SEÇÃO: AÇÕES RÁPIDAS
    # ============================================
    st.markdown("### Ações Rápidas")
    
    if st.button("Limpar Newsletter", use_container_width=True, help="Limpar todos os campos"):
        st.session_state.newsletter_title = ""
        st.session_state.news_items = [{"title": "", "content": ""}]
        st.rerun()
    
    if supabase_manager.connect():
        if st.button("Atualizar Leads", use_container_width=True, help="Recarregar lista de leads"):
            with st.spinner("Atualizando..."):
                supabase_manager.clear_cache()
                st.session_state.leads_data = supabase_manager.get_leads()
            st.success("Atualizado!")
            time.sleep(0.5)
            st.rerun()
            
# Funções auxiliares
def get_logo_base64():
    """Converte a logo da FCP para base64"""
    try:
        logo_path = "logo1_fcp_branco.png"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                return f"data:image/png;base64,{encoded_string}"
        else:
            # Logo padrão se não encontrar o arquivo
            return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMzAiIGZpbGw9IndoaXRlIi8+Cjx0ZXh0IHg9IjMwIiB5PSIzNSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiBmaWxsPSJibGFjayIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RkM8L3RleHQ+Cjwvc3ZnPgo="
    except Exception:
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMzAiIGZpbGw9IndoaXRlIi8+Cjx0ZXh0IHg9IjMwIiB5PSIzNSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiBmaWxsPSJibGFjayIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RkM8L3RleHQ+Cjwvc3ZnPgo="

def generate_html_newsletter(title: str, news_items: List[Dict], date: datetime.date, theme: str, compact_mode: bool = False, layout_style: str = "Moderno") -> str:
    """Gera HTML da newsletter"""
    theme_colors = {
        "Claro": {"bg": "#ffffff", "text": "#333333", "accent": "#007bff"},
        "Escuro": {"bg": "#1a1a1a", "text": "#ffffff", "accent": "#00d4ff"},
        "Azul": {"bg": "#f0f8ff", "text": "#003366", "accent": "#0066cc"},
        "Verde": {"bg": "#f0fff0", "text": "#006600", "accent": "#00aa00"},
        "Roxo": {"bg": "#f8f0ff", "text": "#660066", "accent": "#9900cc"},
        "Federación Poker": {
            "bg": "#ffffff", 
            "text": "#1a1a1a", 
            "accent": "#d32f2f", 
            "secondary": "#1976d2",
            "gold": "#ff9800",
            "light_bg": "#f5f5f5",
            "dark": "#212121",
            "light_gray": "#e0e0e0"
        }
    }
    
    colors = theme_colors.get(theme, theme_colors["Claro"])
    
    if theme == "Federación Poker":
        # Se modo compacto ativado, usar versão ultra-compacta
        if compact_mode:
            return create_ultra_compact_html(title, news_items, date)
        
        logo_base64 = get_logo_base64()
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title or 'Newsletter - Federación Colombiana de Póker'}</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Roboto', Arial, sans-serif; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background: {colors['bg']}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <!-- Header -->
                <div style="background: linear-gradient(135deg, {colors['accent']} 0%, {colors['gold']} 50%, {colors['secondary']} 100%); color: white; padding: 40px 20px; text-align: center; position: relative; overflow: hidden;">
                    <div style="position: relative; z-index: 1;">
                        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 0;">
                            <img src="{logo_base64}" alt="FCP Logo" style="height: 80px; width: auto;" />
                        </div>
                    </div>
                    <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: {colors['gold']};"></div>
                </div>
                
                <!-- Content -->
                <div style="padding: 30px 20px;">
                    {f'<div style="font-size: 24px; font-weight: 700; color: {colors["accent"]}; margin-bottom: 20px; text-align: center;">{title}</div>' if title else ''}
                    
                    {''.join([f'''
                    <div style="margin-bottom: 25px; padding: 20px; background: {colors['bg']}; border: 1px solid {colors['light_gray']}; border-radius: 6px; border-left: 4px solid {colors['accent']};">
                        <h3 style="color: {colors['accent']}; margin-top: 0; margin-bottom: 15px; font-size: 18px; font-weight: 600; text-align: center;">{item["title"]}</h3>
                        <p style="color: {colors['text']}; line-height: 1.6; margin: 0;">{item["content"]}</p>
                    </div>
                    ''' for item in news_items if item["title"] and item["content"]])}
                </div>
                
                <!-- Footer -->
                <div style="background: {colors['dark']}; color: white; padding: 30px 20px; text-align: center;">
                    <h3 style="margin: 0 0 15px 0; font-size: 18px; color: white;">Federación Colombiana de Póker</h3>
                    <div style="margin: 15px 0; font-size: 11px; opacity: 0.8;">
                        Promovemos el poker como deporte mental en Colombia<br>
                        Organizamos torneos, ligas y eventos profesionales
                    </div>
                    <div style="margin: 20px 0;">
                        <a href="https://federacioncolombianadepoker.com.co/pt/" style="color: white; text-decoration: none; margin: 0 10px; font-weight: 500;">🌐 Web</a> |
                        <a href="https://wa.me/573115634142" style="color: white; text-decoration: none; margin: 0 10px; font-weight: 500;">📱 WhatsApp</a>
                    </div>
                    <div style="margin-top: 15px; font-size: 10px; opacity: 0.7;">
                        FCP © 2025
                    </div>
                    <div style="margin-top: 10px;">
                        <a href="https://nexttech-n8n-nexthub.haas2a.easypanel.host/form/ed032453-f1df-42c2-8e5c-ac6ad1b739a7" target="_blank" style="color: #ff6b6b; text-decoration: none; font-size: 10px; opacity: 0.8;">Cancelar inscrição</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    else:
        # Outros temas (Claro, Escuro, Azul, Verde, Rosa)
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title or 'Newsletter'}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: {colors['bg']}; color: {colors['text']}; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background: {colors['accent']}; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ padding: 20px; }}
                .news-item {{ margin-bottom: 20px; padding: 15px; border-left: 4px solid {colors['accent']}; background: #f9f9f9; }}
                .news-item h3 {{ color: {colors['accent']}; margin-top: 0; }}
                .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{title or 'Newsletter'}</h1>
                    <p>Data: {date.strftime('%d/%m/%Y')}</p>
                </div>
                <div class="content">
                    {''.join([f'''
                    <div class="news-item">
                        <h3>{item['title']}</h3>
                        <p>{item['content']}</p>
                    </div>
                    ''' for item in news_items if item['title'] and item['content']])}
                </div>
                <div class="footer">
                    <p>Newsletter gerada automaticamente</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    # Otimizar HTML para evitar corte do Gmail
    return optimize_html_for_email(html)

def generate_markdown_newsletter(title: str, news_items: List[Dict], date: datetime.date) -> str:
    """Gera Markdown da newsletter"""
    markdown = f"# {title or 'Newsletter'}\n\n"
    markdown += f"**Data:** {date.strftime('%d/%m/%Y')}\n\n"
    markdown += "---\n\n"
    
    for item in news_items:
        if item["title"] or item["content"]:
            markdown += f"## {item['title'] or 'Notícia'}\n\n"
            if item["content"]:
                markdown += f"{item['content']}\n\n"
    
    return markdown

def generate_text_newsletter(title: str, news_items: List[Dict], date: datetime.date) -> str:
    """Gera texto simples da newsletter"""
    text = f"{title or 'Newsletter'}\n"
    text += f"Data: {date.strftime('%d/%m/%Y')}\n"
    text += "=" * 50 + "\n\n"
    
    for item in news_items:
        if item["title"] or item["content"]:
            text += f"{item['title'] or 'Notícia'}\n"
            text += "-" * 30 + "\n"
            if item["content"]:
                text += f"{item['content']}\n\n"
    
    return text

def optimize_html_for_email(html_content: str) -> str:
    """Otimiza HTML para evitar corte do Gmail"""
    import re
    
    # Remover espaços em branco desnecessários
    html_content = re.sub(r'\s+', ' ', html_content)
    
    # Remover quebras de linha desnecessárias
    html_content = re.sub(r'>\s+<', '><', html_content)
    
    # Remover comentários HTML
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    
    # Remover espaços antes de tags de fechamento
    html_content = re.sub(r'\s+</', '</', html_content)
    
    return html_content.strip()

def get_html_size_info(html_content: str) -> dict:
    """Retorna informações sobre o tamanho do HTML"""
    size_bytes = len(html_content.encode('utf-8'))
    size_kb = size_bytes / 1024
    
    if size_kb < 50:
        status = "OK"
    elif size_kb < 100:
        status = "GRANDE"
    else:
        status = "MUITO GRANDE"
    
    return {
        "size": f"{size_kb:.1f} KB",
        "status": status,
        "bytes": size_bytes
    }

def create_minimal_html(title: str, news_items: List[Dict], date: datetime.date) -> str:
    """Cria HTML compacto com design bonito da FCP"""
    # HTML com design profissional da FCP - gradiente tricolor e títulos centralizados
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>FCP Newsletter</title></head><body style="font-family:'Segoe UI',Arial,sans-serif;margin:0;padding:0;background:#f5f5f5;"><table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;margin:0 auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.1);"><tr><td style="background:linear-gradient(135deg,#d32f2f 0%,#ff9800 50%,#1976d2 100%);color:#fff;padding:25px;text-align:center;position:relative;"><h1 style="margin:0;font-size:22px;font-weight:600;letter-spacing:0.5px;">Federación Colombiana de Póker</h1><p style="margin:5px 0 0 0;font-size:12px;opacity:0.9;">Newsletter Oficial</p></td></tr><tr><td style="padding:25px;text-align:center;">{f'<h2 style="color:#d32f2f;margin:0 0 30px 0;font-size:20px;font-weight:600;text-align:center;">{title}</h2>' if title else ''}{''.join([f'<div style="margin-bottom:20px;padding:20px;border-left:4px solid #d32f2f;background:#f9f9f9;border-radius:0 8px 8px 0;box-shadow:0 2px 4px rgba(0,0,0,0.05);"><h3 style="color:#d32f2f;margin:0 0 10px 0;font-size:16px;font-weight:600;text-align:center;">{item["title"] or "Notícia"}</h3><p style="margin:0;color:#333;font-size:14px;line-height:1.5;text-align:left;">{item["content"].replace(chr(10), "<br>") if item["content"] else ""}</p></div>' for item in news_items if item["title"] or item["content"]])}</td></tr><tr><td style="background:#212121;color:#fff;padding:20px;text-align:center;"><div style="margin-bottom:10px;"><p style="margin:0;font-size:14px;font-weight:600;">Federación Colombiana de Póker</p><div style="margin:8px 0;font-size:11px;opacity:0.8;">Promovemos el poker como deporte mental en Colombia<br>Organizamos torneos, ligas y eventos profesionales</div></div><div style="margin:15px 0;"><a href="https://federacioncolombianadepoker.com.co/pt/" style="background:#ff9800;color:#fff;padding:8px 16px;text-decoration:none;border-radius:20px;font-size:12px;font-weight:500;margin:0 5px;display:inline-block;">🌐 Web</a><a href="https://wa.me/573115634142" style="background:#25d366;color:#fff;padding:8px 16px;text-decoration:none;border-radius:20px;font-size:12px;font-weight:500;margin:0 5px;display:inline-block;">📱 WhatsApp</a></div><div style="margin-top:10px;font-size:10px;opacity:0.7;">FCP © 2025</div><div style="margin-top:8px;"><a href="#" href="https://nexttech-n8n-nexthub.haas2a.easypanel.host/form/ed032453-f1df-42c2-8e5c-ac6ad1b739a7" target="_blank" style="color: #ff6b6b; text-decoration: none; font-size: 10px; opacity: 0.8;">Cancelar inscrição</a></div></td></tr></table>
        
        </body></html>"""
    
    return optimize_html_for_email(html)

def create_ultra_compact_html(title: str, news_items: List[Dict], date: datetime.date) -> str:
    """Cria HTML ultra-compacto com design bonito da FCP"""
    # Versão ultra-compacta com gradiente tricolor e títulos centralizados
    header = f"<div style='background:linear-gradient(135deg,#d32f2f 0%,#ff9800 50%,#1976d2 100%);color:#fff;padding:15px;text-align:center;border-radius:8px 8px 0 0;'><h1 style='margin:0;font-size:18px;font-weight:600;'>Federación Colombiana de Póker</h1></div>"
    
    title_section = f"<h2 style='color:#d32f2f;margin:0 0 20px 0;font-size:18px;font-weight:600;text-align:center;'>{title}</h2>" if title else ""
    content = f"<div style='padding:20px;background:#fff;text-align:center;'>{title_section}"
    
    for item in news_items:
        if item["title"] or item["content"]:
            content += f"<div style='margin-bottom:15px;padding:15px;border-left:3px solid #d32f2f;background:#f9f9f9;border-radius:0 6px 6px 0;'><h3 style='color:#d32f2f;margin:0 0 8px 0;font-size:14px;font-weight:600;text-align:center;'>{item['title'] or 'Notícia'}</h3><p style='margin:0;color:#333;font-size:13px;line-height:1.4;text-align:left;'>{item['content'].replace(chr(10), '<br>') if item['content'] else ''}</p></div>"
    
    content += "</div>"
    
    footer = f"<div style='background:#212121;color:#fff;padding:15px;text-align:center;border-radius:0 0 8px 8px;'><div style='margin:5px 0;font-size:10px;opacity:0.8;'>Promovemos el poker como deporte mental en Colombia<br>Organizamos torneos, ligas y eventos profesionales</div><div style='margin:10px 0;'><a href='https://federacioncolombianadepoker.com.co/pt/' style='background:#ff9800;color:#fff;padding:6px 12px;text-decoration:none;border-radius:15px;font-size:11px;margin:0 3px;display:inline-block;'>🌐 Web</a><a href='https://wa.me/573115634142' style='background:#25d366;color:#fff;padding:6px 12px;text-decoration:none;border-radius:15px;font-size:11px;margin:0 3px;display:inline-block;'>📱 WhatsApp</a></div><p style='margin:8px 0 0 0;font-size:10px;opacity:0.7;'>FCP © 2025</p><div style='margin-top:6px;'><a href='https://nexttech-n8n-nexthub.haas2a.easypanel.host/form/ed032453-f1df-42c2-8e5c-ac6ad1b739a7' target='_blank' style='color: #ff6b6b; text-decoration: none; font-size: 9px; opacity: 0.8;'>Cancelar inscrição</a></div></div>"
    
    modal_html = """
        <!-- Modal de Cancelamento de Inscrição -->
        <div id='unsubscribeModal' style='display: none; position: fixed; z-index: 10000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); backdrop-filter: blur(5px);'>
            <div style='position: relative; background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); margin: 10% auto; padding: 0; border: none; width: 90%; max-width: 450px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; animation: modalSlideIn 0.3s ease-out;'>
                <!-- Header do Modal -->
                <div style='background: linear-gradient(135deg, #d32f2f 0%, #ff9800 50%, #1976d2 100%); padding: 30px 20px; text-align: center; position: relative;'>
                    <div style='width: 60px; height: 60px; background: rgba(255,255,255,0.2); border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 30px; color: white;'>
                        ✉️
                    </div>
                    <h2 style='color: white; margin: 0; font-size: 22px; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>Cancelar Inscrição</h2>
                </div>
                
                <!-- Conteúdo do Modal -->
                <div style='padding: 30px 25px;'>
                    <p style='text-align: center; margin: 0 0 20px 0; color: #555; font-size: 16px; line-height: 1.5;'>
                        Tem certeza de que deseja cancelar sua inscrição na newsletter da FCP?
                    </p>
                    
                    <div style='background: #f8f9fa; border-left: 4px solid #d32f2f; padding: 15px; margin: 20px 0; border-radius: 0 8px 8px 0;'>
                        <p style='margin: 0; color: #666; font-size: 14px;'>
                            <strong>O que isso significa:</strong><br>
                            Você não receberá mais nossas newsletters sobre poker, torneios e eventos.
                        </p>
                    </div>
                    
                    <!-- Campo de Email -->
                    <div style='margin: 20px 0;'>
                        <label style='display: block; margin-bottom: 8px; color: #333; font-weight: 500; font-size: 14px;'>Seu Email:</label>
                        <input type='email' id='unsubscribeEmail' placeholder='seu@email.com' style='width: 100%; padding: 12px 15px; border: 2px solid #e1e5e9; border-radius: 10px; font-size: 14px; transition: border-color 0.3s; box-sizing: border-box;' onfocus='this.style.borderColor=\'#d32f2f\'' onblur='this.style.borderColor=\'#e1e5e9\''>
                    </div>
                    
                    <!-- Botões -->
                    <div style='display: flex; gap: 12px; margin-top: 25px;'>
                        <button onclick='confirmUnsubscribe()' style='flex: 1; background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%); color: white; border: none; padding: 12px 20px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 15px rgba(211, 47, 47, 0.3);'>
                            Sim, Cancelar
                        </button>
                        <button onclick='hideUnsubscribeModal()' style='flex: 1; background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%); color: white; border: none; padding: 12px 20px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);'>
                            Manter Inscrito
                        </button>
                    </div>
                </div>
                
                <!-- Footer do Modal -->
                <div style='background: #f8f9fa; padding: 15px 25px; text-align: center; border-top: 1px solid #e9ecef;'>
                    <p style='margin: 0; color: #999; font-size: 12px;'>
                        Federación Colombiana de Póker © 2025
                    </p>
                </div>
            </div>
        </div>
        
        <style>
        @keyframes modalSlideIn {
            from {
                opacity: 0;
                transform: translateY(-50px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        #unsubscribeModal button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        }
        
        #unsubscribeModal input:focus {
            outline: none;
            box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.1);
        }
        </style>
        
        <script>
        function showUnsubscribeModal() {
            document.getElementById('unsubscribeModal').style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
        
        function hideUnsubscribeModal() {
            document.getElementById('unsubscribeModal').style.display = 'none';
            document.body.style.overflow = 'auto';
            document.getElementById('unsubscribeEmail').value = '';
        }
        
        function confirmUnsubscribe() {
            const email = document.getElementById('unsubscribeEmail').value.trim();
            
            if (!email) {
                alert('Por favor, digite seu email para continuar.');
                return;
            }
            
            if (!isValidEmail(email)) {
                alert('Por favor, digite um email válido.');
                return;
            }
            
            const button = event.target;
            const originalText = button.textContent;
            button.textContent = 'Processando...';
            button.disabled = true;
            
            setTimeout(() => {
                alert('Inscrição cancelada com sucesso!\\n\\nVocê não receberá mais nossas newsletters.');
                hideUnsubscribeModal();
                button.textContent = originalText;
                button.disabled = false;
            }, 1500);
        }
        
        function isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }
        
        window.onclick = function(event) {
            const modal = document.getElementById('unsubscribeModal');
            if (event.target == modal) {
                hideUnsubscribeModal();
            }
        }
        
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                hideUnsubscribeModal();
            }
        });
        </script>"""
    
    html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>FCP Newsletter</title></head><body style='font-family:Segoe UI,Arial,sans-serif;margin:0;padding:10px;background:#f5f5f5;'><div style='max-width:600px;margin:0 auto;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);'>{header}{content}{footer}</div>{modal_html}</body></html>"
    
    return optimize_html_for_email(html)

def get_theme_styles(theme: str) -> str:
    """Retorna estilos CSS para o tema selecionado"""
    theme_styles = {
        "Claro": {
            "bg": "#ffffff",
            "text": "#333333", 
            "accent": "#007bff",
            "border": "#e0e0e0"
        },
        "Escuro": {
            "bg": "#1a1a1a",
            "text": "#ffffff",
            "accent": "#00d4ff", 
            "border": "#333333"
        },
        "Azul": {
            "bg": "#f0f8ff",
            "text": "#003366",
            "accent": "#0066cc",
            "border": "#b3d9ff"
        },
        "Verde": {
            "bg": "#f0fff0",
            "text": "#006600",
            "accent": "#00aa00",
            "border": "#b3ffb3"
        },
        "Roxo": {
            "bg": "#f8f0ff",
            "text": "#660066",
            "accent": "#9900cc",
            "border": "#e6b3ff"
        }
    }
    
    colors = theme_styles.get(theme, theme_styles["Claro"])
    
    return f"""
    <style>
    .newsletter-preview {{
        background-color: {colors['bg']};
        color: {colors['text']};
        padding: 20px;
        border-radius: 10px;
        border: 2px solid {colors['border']};
        font-family: Arial, sans-serif;
        line-height: 1.6;
    }}
    .newsletter-preview h1 {{
        color: {colors['accent']};
        border-bottom: 3px solid {colors['accent']};
        padding-bottom: 10px;
        text-align: center;
    }}
    .newsletter-preview h2 {{
        color: {colors['accent']};
        border-left: 4px solid {colors['accent']};
        padding-left: 15px;
        margin-top: 25px;
    }}
    .newsletter-preview .date {{
        color: #666;
        font-style: italic;
        text-align: center;
        margin: 10px 0;
    }}
    .newsletter-preview .news-item {{
        margin: 20px 0;
        padding: 15px;
        background-color: rgba(0,0,0,0.02);
        border-radius: 5px;
    }}
    .newsletter-preview hr {{
        border: 1px solid {colors['border']};
        margin: 20px 0;
    }}
    .newsletter-preview .footer {{
        text-align: center;
        color: #666;
        font-style: italic;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid {colors['border']};
    }}
    </style>
    """

def handle_unsubscribe():
    """Processa cancelamento de inscrição via URL"""
    query_params = st.query_params
    
    if query_params.get("action") == "unsubscribe":
        email = query_params.get("email")
        
        if not email:
            # Mostrar página de cancelamento
            show_unsubscribe_page()
            return True
        
        # Processar cancelamento
        if supabase_manager and supabase_manager.connect():
            result = supabase_manager.process_unsubscribe(email)
            
            if result['success']:
                st.success(f"✅ {result['message']}")
                st.balloons()
            else:
                st.error(f"❌ {result['message']}")
        else:
            st.error("Erro de conexão com o banco de dados")
        
        # Limpar parâmetros da URL
        st.query_params.clear()
        return True
    
    return False

def show_unsubscribe_page():
    """Mostra página de cancelamento de inscrição"""
    st.set_page_config(
        page_title="Cancelar Inscrição - FCP",
        page_icon="✉️",
        layout="centered"
    )
    
    # CSS para página de cancelamento
    st.markdown("""
    <style>
    .unsubscribe-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 40px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    .unsubscribe-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #d32f2f 0%, #ff9800 50%, #1976d2 100%);
        border-radius: 50%;
        margin: 0 auto 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        color: white;
    }
    .unsubscribe-title {
        color: #d32f2f;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 20px;
    }
    .unsubscribe-subtitle {
        color: #666;
        font-size: 16px;
        margin-bottom: 30px;
        line-height: 1.5;
    }
    .unsubscribe-info {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        color: #666;
        font-size: 14px;
    }
    .unsubscribe-footer {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        color: #999;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container principal
    st.markdown('<div class="unsubscribe-container">', unsafe_allow_html=True)
    
    # Ícone
    st.markdown('<div class="unsubscribe-icon">✉️</div>', unsafe_allow_html=True)
    
    # Título
    st.markdown('<h1 class="unsubscribe-title">Cancelar Inscrição</h1>', unsafe_allow_html=True)
    
    # Formulário de email
    st.markdown('<p class="unsubscribe-subtitle">Digite seu email para cancelar a inscrição na nossa newsletter:</p>', unsafe_allow_html=True)
    
    with st.form("unsubscribe_form"):
        email = st.text_input(
            "Email",
            placeholder="seu@email.com",
            help="Digite o email que deseja remover da nossa lista"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            confirm_unsubscribe = st.form_submit_button(
                "Sim, Cancelar Inscrição",
                type="primary",
                use_container_width=True
            )
        
        with col2:
            keep_subscribed = st.form_submit_button(
                "Não, Manter Inscrito",
                type="secondary",
                use_container_width=True
            )
    
    # Processar formulário
    if confirm_unsubscribe and email:
        if supabase_manager and supabase_manager.connect():
            result = supabase_manager.process_unsubscribe(email)
            
            if result['success']:
                st.success(f"✅ {result['message']}")
                st.balloons()
            else:
                st.error(f"❌ {result['message']}")
        else:
            st.error("❌ Erro de conexão com o banco de dados")
    
    elif keep_subscribed:
        st.info("✅ Você permanece inscrito na nossa newsletter!")
        st.markdown('<a href="https://federacioncolombianadepoker.com.co/pt/" target="_blank">Visitar Website da FCP</a>', unsafe_allow_html=True)
    
    # Informações
    st.markdown("""
    <div class="unsubscribe-info">
        <strong>O que isso significa?</strong><br>
        Você não receberá mais nossas newsletters da Federación Colombiana de Póker.
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="unsubscribe-footer">
        Federación Colombiana de Póker © 2025<br>
        <a href="https://federacioncolombianadepoker.com.co/pt/" style="color: #d32f2f; text-decoration: none;">Visitar Website</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Verificar se é uma requisição de cancelamento de inscrição
if handle_unsubscribe():
    st.stop()

# Aplicar tema do site
def apply_site_theme():
    """Aplica o tema claro/escuro do site"""
    if st.session_state.site_dark_mode:
        st.markdown("""
        <style>
        /* Tema escuro melhorado */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e8e8e8;
        }
        .main .block-container {
            background: transparent;
            color: #e8e8e8;
            padding-top: 2rem;
        }
        .stSidebar {
            background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
            border-right: 1px solid #4a5568;
        }
        .stSidebar .sidebar-content {
            background: transparent;
        }
        
        /* Textos da sidebar no tema escuro */
        .stSidebar .stMarkdown {
            color: #ffffff !important;
        }
        .stSidebar .stMarkdown h1, 
        .stSidebar .stMarkdown h2, 
        .stSidebar .stMarkdown h3,
        .stSidebar .stMarkdown h4,
        .stSidebar .stMarkdown h5,
        .stSidebar .stMarkdown h6 {
            color: #ffffff !important;
        }
        .stSidebar .stText {
            color: #ffffff !important;
        }
        .stSidebar .stLabel {
            color: #ffffff !important;
        }
        .stSidebar .stSelectbox label {
            color: #ffffff !important;
        }
        .stSidebar .stDateInput label {
            color: #ffffff !important;
        }
        .stSidebar .stTextInput label {
            color: #ffffff !important;
        }
        .stSidebar .stTextArea label {
            color: #ffffff !important;
        }
        .stSidebar .stButton label {
            color: #ffffff !important;
        }
        .stSidebar .stToggle label {
            color: #ffffff !important;
        }
        .stSidebar .stCaption {
            color: #a0aec0 !important;
        }
        .stSidebar .stHelp {
            color: #a0aec0 !important;
        }
        
        /* Garantir que todos os textos da sidebar sejam brancos */
        .stSidebar * {
            color: #ffffff !important;
        }
        .stSidebar .stMarkdown * {
            color: #ffffff !important;
        }
        .stSidebar .stText * {
            color: #ffffff !important;
        }
        .stSidebar .stLabel * {
            color: #ffffff !important;
        }
        .stSidebar .stCaption {
            color: #a0aec0 !important;
        }
        .stSidebar .stHelp {
            color: #a0aec0 !important;
        }
        .stSidebar .stTextInput > div > div > input {
            color: #e8e8e8 !important;
        }
        .stSidebar .stTextArea > div > div > textarea {
            color: #e8e8e8 !important;
        }
        .stSidebar .stSelectbox > div > div {
            color: #e8e8e8 !important;
        }
        .stSidebar .stDateInput > div > div > input {
            color: #e8e8e8 !important;
        }
        
        /* Garantir que todos os placeholders sejam brancos no tema escuro */
        input::placeholder,
        input::-webkit-input-placeholder,
        input::-moz-placeholder,
        input:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        textarea::placeholder,
        textarea::-webkit-input-placeholder,
        textarea::-moz-placeholder,
        textarea:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        .stTextInput input::placeholder,
        .stTextInput input::-webkit-input-placeholder,
        .stTextInput input::-moz-placeholder,
        .stTextInput input:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        .stTextArea textarea::placeholder,
        .stTextArea textarea::-webkit-input-placeholder,
        .stTextArea textarea::-moz-placeholder,
        .stTextArea textarea:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        /* Seletores mais específicos para Streamlit */
        .stApp input::placeholder,
        .stApp input::-webkit-input-placeholder,
        .stApp input::-moz-placeholder,
        .stApp input:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        .stApp textarea::placeholder,
        .stApp textarea::-webkit-input-placeholder,
        .stApp textarea::-moz-placeholder,
        .stApp textarea:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        /* Forçar cor dos placeholders com seletores mais específicos */
        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stTextInput"] input::-webkit-input-placeholder,
        div[data-testid="stTextInput"] input::-moz-placeholder,
        div[data-testid="stTextInput"] input:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        div[data-testid="stTextArea"] textarea::placeholder,
        div[data-testid="stTextArea"] textarea::-webkit-input-placeholder,
        div[data-testid="stTextArea"] textarea::-moz-placeholder,
        div[data-testid="stTextArea"] textarea:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        
        /* Inputs e formulários */
        .stTextInput > div > div > input {
            background-color: #2d3748 !important;
            color: #e8e8e8 !important;
            border: 2px solid #4a5568 !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #63b3ed !important;
            box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.1) !important;
        }
        .stTextInput > div > div > input::placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        
        /* Forçar cor dos placeholders com máxima especificidade */
        .stApp .main .block-container .stTextInput input::placeholder,
        .stApp .main .block-container .stTextInput input::-webkit-input-placeholder,
        .stApp .main .block-container .stTextInput input::-moz-placeholder,
        .stApp .main .block-container .stTextInput input:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        
        .stApp .main .block-container .stTextArea textarea::placeholder,
        .stApp .main .block-container .stTextArea textarea::-webkit-input-placeholder,
        .stApp .main .block-container .stTextArea textarea::-moz-placeholder,
        .stApp .main .block-container .stTextArea textarea:-ms-input-placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        
        .stTextArea > div > div > textarea {
            background-color: #2d3748 !important;
            color: #e8e8e8 !important;
            border: 2px solid #4a5568 !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }
        .stTextArea > div > div > textarea:focus {
            border-color: #63b3ed !important;
            box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.1) !important;
        }
        .stTextArea > div > div > textarea::placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        
        .stSelectbox > div > div {
            background-color: #2d3748 !important;
            color: #e8e8e8 !important;
            border: 2px solid #4a5568 !important;
            border-radius: 8px !important;
        }
        .stSelectbox > div > div:focus-within {
            border-color: #63b3ed !important;
            box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.1) !important;
        }
        
        .stDateInput > div > div > input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #4a5568 !important;
            border-radius: 8px !important;
        }
        .stDateInput > div > div > input:focus {
            border-color: #63b3ed !important;
            box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.1) !important;
        }
        .stDateInput > div > div > input::placeholder {
            color: #666666 !important;
            opacity: 1 !important;
        }
        
        /* Estilos específicos para o campo de data no tema escuro */
        .stDateInput input {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stDateInput input[type="text"] {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stDateInput input[value] {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stDateInput .stDateInput > div > div > input {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        /* Garantir que todos os elementos do DateInput sejam legíveis */
        .stDateInput * {
            color: #000000 !important;
        }
        .stDateInput input {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        /* Botões */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stDownloadButton > button {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        .stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(240, 147, 251, 0.4) !important;
        }
        
        /* Expanders */
        .stExpander > div {
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%) !important;
            border: 1px solid #4a5568 !important;
            border-radius: 12px !important;
            margin: 0.5rem 0 !important;
        }
        .stExpander > div > div {
            background: transparent !important;
        }
        .stExpander > div > div > div {
            background: transparent !important;
        }
        
        /* Toggle */
        .stToggle > div > div {
            background-color: #4a5568 !important;
        }
        .stToggle > div > div[data-checked="true"] {
            background-color: #63b3ed !important;
        }
        
        /* Textos e labels */
        .stMarkdown {
            color: #e8e8e8 !important;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #ffffff !important;
        }
        
        /* Alertas e notificações */
        .stInfo {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 8px !important;
            color: #e8e8e8 !important;
        }
        .stWarning {
            background: linear-gradient(135deg, #92400e 0%, #b45309 100%) !important;
            border: 1px solid #f59e0b !important;
            border-radius: 8px !important;
            color: #e8e8e8 !important;
        }
        .stSuccess {
            background: linear-gradient(135deg, #065f46 0%, #047857 100%) !important;
            border: 1px solid #10b981 !important;
            border-radius: 8px !important;
            color: #e8e8e8 !important;
        }
        .stError {
            background: linear-gradient(135deg, #991b1b 0%, #dc2626 100%) !important;
            border: 1px solid #ef4444 !important;
            border-radius: 8px !important;
            color: #e8e8e8 !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #2d3748 !important;
            border-radius: 8px !important;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            color: #a0aec0 !important;
            border-radius: 6px !important;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #ffffff !important;
        }
        
        /* Containers */
        .stContainer {
            background: transparent !important;
        }
        
        /* DataFrames */
        .stDataFrame {
            background-color: #2d3748 !important;
            border-radius: 8px !important;
        }
        .stDataFrame table {
            background-color: #2d3748 !important;
            color: #e8e8e8 !important;
        }
        .stDataFrame th {
            background-color: #4a5568 !important;
            color: #ffffff !important;
        }
        .stDataFrame td {
            background-color: #2d3748 !important;
            color: #e8e8e8 !important;
        }
        
        /* Code blocks */
        .stCodeBlock {
            background-color: #1a202c !important;
            border-radius: 8px !important;
        }
        .stCodeBlock pre {
            background-color: #1a202c !important;
            color: #e8e8e8 !important;
        }
        
        /* Captions */
        .stCaption {
            color: #a0aec0 !important;
        }
        
        /* Scrollbar personalizada */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #2d3748;
        }
        ::-webkit-scrollbar-thumb {
            background: #4a5568;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #63b3ed;
        }
        
        /* Estilo para mensagem de preview vazio no tema escuro */
        .preview-empty {
            text-align: center;
            padding: 2rem;
            color: #a0aec0 !important;
            font-style: italic;
            background: transparent !important;
        }
        
        /* CSS removido para permitir exibição da tabela */
        </style>
        <script>
        // JavaScript para forçar cor dos placeholders e campos de data no tema escuro
        function updatePlaceholders() {
            const inputs = document.querySelectorAll('input[placeholder]');
            const textareas = document.querySelectorAll('textarea[placeholder]');
            const dateInputs = document.querySelectorAll('.stDateInput input');
            
            inputs.forEach(input => {
                input.style.setProperty('--placeholder-color', '#ffffff', 'important');
                input.style.setProperty('color', '#ffffff', 'important');
                input.setAttribute('style', input.getAttribute('style') + '; color: #ffffff !important;');
            });
            
            textareas.forEach(textarea => {
                textarea.style.setProperty('--placeholder-color', '#ffffff', 'important');
                textarea.style.setProperty('color', '#ffffff', 'important');
                textarea.setAttribute('style', textarea.getAttribute('style') + '; color: #ffffff !important;');
            });
            
            // Forçar campo de data a ter fundo branco e texto preto
            dateInputs.forEach(input => {
                input.style.setProperty('background-color', '#ffffff', 'important');
                input.style.setProperty('color', '#000000', 'important');
                input.setAttribute('style', input.getAttribute('style') + '; background-color: #ffffff !important; color: #000000 !important;');
            });
        }
        
        // Função para remover elementos vazios que criam barras brancas
        // JavaScript removido para permitir exibição da tabela
        
        // Executar quando a página carregar
        document.addEventListener('DOMContentLoaded', function() {
            updatePlaceholders();
        });
        
        // Executar quando houver mudanças no DOM
        const observer = new MutationObserver(function() {
            updatePlaceholders();
        });
        observer.observe(document.body, { childList: true, subtree: true });
        </script>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        /* Tema claro melhorado */
        .stApp {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 50%, #e2e8f0 100%);
            color: #2d3748;
        }
        .main .block-container {
            background: transparent;
            color: #2d3748;
            padding-top: 2rem;
        }
        .stSidebar {
            background: linear-gradient(180deg, #ffffff 0%, #f7fafc 100%);
            border-right: 1px solid #e2e8f0;
        }
        .stSidebar .sidebar-content {
            background: transparent;
        }
        
        /* Textos da sidebar no tema claro */
        .stSidebar .stMarkdown {
            color: #2d3748 !important;
        }
        .stSidebar .stMarkdown h1, 
        .stSidebar .stMarkdown h2, 
        .stSidebar .stMarkdown h3,
        .stSidebar .stMarkdown h4,
        .stSidebar .stMarkdown h5,
        .stSidebar .stMarkdown h6 {
            color: #1a202c !important;
        }
        .stSidebar .stText {
            color: #2d3748 !important;
        }
        .stSidebar .stLabel {
            color: #2d3748 !important;
        }
        .stSidebar .stSelectbox label {
            color: #2d3748 !important;
        }
        .stSidebar .stDateInput label {
            color: #2d3748 !important;
        }
        .stSidebar .stTextInput label {
            color: #2d3748 !important;
        }
        .stSidebar .stTextArea label {
            color: #2d3748 !important;
        }
        .stSidebar .stButton label {
            color: #2d3748 !important;
        }
        .stSidebar .stToggle label {
            color: #2d3748 !important;
        }
        .stSidebar .stCaption {
            color: #718096 !important;
        }
        .stSidebar .stHelp {
            color: #718096 !important;
        }
        
        /* Inputs e formulários */
        .stTextInput > div > div > input {
            background-color: #ffffff !important;
            color: #2d3748 !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #4299e1 !important;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1) !important;
        }
        .stTextInput > div > div > input::placeholder {
            color: #718096 !important;
            opacity: 1 !important;
        }
        
        .stTextArea > div > div > textarea {
            background-color: #ffffff !important;
            color: #2d3748 !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }
        .stTextArea > div > div > textarea:focus {
            border-color: #4299e1 !important;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1) !important;
        }
        .stTextArea > div > div > textarea::placeholder {
            color: #718096 !important;
            opacity: 1 !important;
        }
        
        .stSelectbox > div > div {
            background-color: #ffffff !important;
            color: #2d3748 !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }
        .stSelectbox > div > div:focus-within {
            border-color: #4299e1 !important;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1) !important;
        }
        
        .stDateInput > div > div > input {
            background-color: #ffffff !important;
            color: #2d3748 !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }
        .stDateInput > div > div > input:focus {
            border-color: #4299e1 !important;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1) !important;
        }
        
        /* Botões */
        .stButton > button {
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(66, 153, 225, 0.4) !important;
        }
        
        .stDownloadButton > button {
            background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        .stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(237, 137, 54, 0.4) !important;
        }
        
        /* Expanders */
        .stExpander > div {
            background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%) !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            margin: 0.5rem 0 !important;
        }
        .stExpander > div > div {
            background: transparent !important;
        }
        .stExpander > div > div > div {
            background: transparent !important;
        }
        
        /* Toggle */
        .stToggle > div > div {
            background-color: #cbd5e0 !important;
        }
        .stToggle > div > div[data-checked="true"] {
            background-color: #4299e1 !important;
        }
        
        /* Textos e labels */
        .stMarkdown {
            color: #2d3748 !important;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #1a202c !important;
        }
        
        /* Alertas e notificações */
        .stInfo {
            background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%) !important;
            border: 1px solid #90cdf4 !important;
            border-radius: 8px !important;
            color: #2c5282 !important;
        }
        .stWarning {
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%) !important;
            border: 1px solid #f6e05e !important;
            border-radius: 8px !important;
            color: #92400e !important;
        }
        .stSuccess {
            background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%) !important;
            border: 1px solid #9ae6b4 !important;
            border-radius: 8px !important;
            color: #22543d !important;
        }
        .stError {
            background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%) !important;
            border: 1px solid #fc8181 !important;
            border-radius: 8px !important;
            color: #742a2a !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f7fafc !important;
            border-radius: 8px !important;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            color: #718096 !important;
            border-radius: 6px !important;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
            color: #ffffff !important;
        }
        
        /* Containers */
        .stContainer {
            background: transparent !important;
        }
        
        /* DataFrames */
        .stDataFrame {
            background-color: #ffffff !important;
            border-radius: 8px !important;
        }
        .stDataFrame table {
            background-color: #ffffff !important;
            color: #2d3748 !important;
        }
        .stDataFrame th {
            background-color: #f7fafc !important;
            color: #1a202c !important;
        }
        .stDataFrame td {
            background-color: #ffffff !important;
            color: #2d3748 !important;
        }
        
        /* Code blocks */
        .stCodeBlock {
            background-color: #f7fafc !important;
            border-radius: 8px !important;
        }
        .stCodeBlock pre {
            background-color: #f7fafc !important;
            color: #2d3748 !important;
        }
        
        /* Captions */
        .stCaption {
            color: #718096 !important;
        }
        
        /* Scrollbar personalizada */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f7fafc;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #4299e1;
        }
        
        /* Estilo para mensagem de preview vazio no tema claro */
        .preview-empty {
            text-align: center;
            padding: 2rem;
            color: #718096 !important;
            font-style: italic;
            background: transparent !important;
        }
        
        /* CSS removido para permitir exibição da tabela */
        </style>
        """, unsafe_allow_html=True)

# Aplicar tema do site
apply_site_theme()

# Criar abas para organizar as funcionalidades
tab1, tab2, tab3 = st.tabs(["Editor", "Leads", "Enviar"])

with tab1:
    # Seção principal do editor
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Editor da Newsletter")
        
        # Título da newsletter
        st.subheader("Título da Newsletter")
        newsletter_title = st.text_input(
            "Digite o título da newsletter:",
            value=st.session_state.newsletter_title,
            placeholder="Ex: Notícias da Semana - Edição 123"
        )
        st.session_state.newsletter_title = newsletter_title
        
        st.markdown("---")
        
        # Seção de notícias
        st.subheader("Notícias")
        
        # Lista de notícias
        for i, news_item in enumerate(st.session_state.news_items):
            with st.expander(f"Notícia {i+1}", expanded=True):
                # Título da notícia
                news_title = st.text_input(
                    f"Título da Notícia {i+1}:",
                    value=news_item["title"],
                    key=f"news_title_{i}",
                    placeholder="Digite o título da notícia..."
                )
                
                # Conteúdo da notícia
                news_content = st.text_area(
                    f"Conteúdo da Notícia {i+1}:",
                    value=news_item["content"],
                    key=f"news_content_{i}",
                    placeholder="Digite o conteúdo da notícia...",
                    height=150
                )
                
                # Atualizar dados da notícia
                st.session_state.news_items[i] = {
                    "title": news_title,
                    "content": news_content
                }
                
                # Botão para remover notícia (se houver mais de uma)
                if len(st.session_state.news_items) > 1:
                    if st.button(f"🗑️ Remover Notícia {i+1}", key=f"remove_{i}"):
                        st.session_state.news_items.pop(i)
                        st.rerun()
        
        # Botão para adicionar nova notícia
        if st.button("➕ Adicionar Nova Notícia", type="primary"):
            st.session_state.news_items.append({"title": "", "content": ""})
            st.rerun()

    with col2:
        st.header("Preview")
        
        # Preview da newsletter
        if newsletter_title or any(item["title"] or item["content"] for item in st.session_state.news_items):
            # Gerar preview HTML
            html_content = generate_html_newsletter(newsletter_title, st.session_state.news_items, newsletter_date, theme, compact_mode, layout_style)
            
            # Mostrar informações de tamanho
            size_info = get_html_size_info(html_content)
            st.info(f"📊 Tamanho do HTML: {size_info['size']} | Status: {size_info['status']}")
            
            # Mostrar preview HTML
            st.markdown(html_content, unsafe_allow_html=True)
        else:
            st.info("Adicione um título e pelo menos uma notícia para ver o preview")
    
# Aba de Gerenciamento de Leads
with tab2:
    st.header("Gerenciar Leads")
    
    supabase_url, supabase_key = get_supabase_config()
    
    if not supabase_url or not supabase_key:
        st.warning("Configure o Supabase na sidebar para gerenciar leads")
    else:
        # Conectar ao Supabase
        if supabase_manager.connect():
            st.success("Conectado ao Supabase")
            
            # Atualizar dados dos leads
            if st.button("Atualizar Lista de Leads"):
                with st.spinner("Carregando leads do Supabase..."):
                    supabase_manager.clear_cache()  # Limpar cache
                    st.session_state.leads_data = supabase_manager.get_leads()
                st.rerun()
            
            # Carregar leads
            with st.spinner("Carregando leads..."):
                leads_df = supabase_manager.get_leads_dataframe()
            
            # Mostrar estatísticas
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total de Leads", len(leads_df))
            with col2:
                st.metric("Emails Únicos", leads_df['email'].nunique() if 'email' in leads_df.columns else 0)
            
            # Tabela de leads
            st.subheader("Leads")
            
            if not leads_df.empty:
                st.dataframe(
                    leads_df,
                    width='stretch',
                    hide_index=True
                )
            else:
                st.info("Nenhum lead encontrado")
            
            # Adicionar novo lead
            st.subheader("Adicionar Novo Lead")
            with st.form("add_lead_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_email = st.text_input("Email", placeholder="exemplo@email.com")
                with col2:
                    new_name = st.text_input("Nome (opcional)", placeholder="Nome do lead")
                
                if st.form_submit_button("➕ Adicionar Lead", type="primary"):
                    if new_email:
                        if supabase_manager.add_lead(new_email, new_name):
                            st.success(f"✅ Lead {new_email} adicionado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao adicionar lead")
                    else:
                        st.error("⚠️ Email é obrigatório")
        else:
            st.error("❌ Erro ao conectar com Supabase")

# Aba de Envio de Newsletter
with tab3:
    st.header("Enviar Newsletter")
    
    # Verificar se há conteúdo para enviar
    has_content = newsletter_title or any(item["title"] or item["content"] for item in st.session_state.news_items)
    
    if not has_content:
        st.warning("Adicione uma notícia na aba 'Editor'")
    else:
        supabase_url, supabase_key = get_supabase_config()
        
        if not supabase_url or not supabase_key:
            st.warning("Configure o Supabase na sidebar para enviar newsletter")
        else:
            # Conectar ao Supabase
            if supabase_manager.connect():
                st.success("✅ Conectado ao Supabase")
                
                # Obter leads inscritos
                with st.spinner("Carregando leads inscritos..."):
                    subscribed_leads = supabase_manager.get_subscribed_leads()
                
                if not subscribed_leads:
                    st.warning("Nenhum lead inscrito encontrado. Adicione leads na aba 'Leads'")
                else:
                    st.success(f"{len(subscribed_leads)} leads inscritos encontrados")
                    
                    # Preview da newsletter que será enviada
                    st.subheader("📋 Preview da Newsletter")
                    st.markdown("**Título:** " + (newsletter_title or "Sem título"))
                    st.markdown("**Data:** " + newsletter_date.strftime("%d/%m/%Y"))
                    st.markdown("**Número de notícias:** " + str(len([item for item in st.session_state.news_items if item["title"] or item["content"]])))
                    
                    # Configurações de envio
                    st.subheader("⚙️ Configurações de Envio")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        email_subject = st.text_input(
                            "Assunto do Email",
                            value=newsletter_title or "Newsletter",
                            placeholder="Assunto do email"
                        )
                    with col2:
                        test_email = st.text_input(
                            "Email de Teste (opcional)",
                            placeholder="teste@email.com",
                            help="Envie um teste antes de enviar para todos"
                        )
                    
                    # Botões de ação com melhor espaçamento
                    st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço extra
                    
                    # CSS para alinhar botões
                    st.markdown("""
                    <style>
                    .align-left { text-align: left; }
                    .align-center { text-align: center; }
                    .align-right { text-align: right; }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([3, 2, 3], gap="large")
                    
                    with col1:
                        st.markdown('<div class="align-left">', unsafe_allow_html=True)
                        st.markdown("### 🧪 Teste")
                        st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço antes do botão
                        if test_email and st.button("🧪 Enviar Teste", type="secondary", width='stretch'):
                            if email_manager.test_connection():
                                # Gerar newsletter
                                html_content = generate_html_newsletter(newsletter_title, st.session_state.news_items, newsletter_date, theme, compact_mode, layout_style)
                                text_content = generate_text_newsletter(newsletter_title, st.session_state.news_items, newsletter_date)
                                
                                # Enviar teste
                                test_recipients = [{"email": test_email, "name": "Teste"}]
                                results = email_manager.send_newsletter(html_content, text_content, test_recipients, email_subject)
                                
                                if results['sent'] > 0:
                                    st.success(f"✅ Email de teste enviado para {test_email}")
                                else:
                                    st.error(f"❌ Erro ao enviar teste: {', '.join(results['errors'])}")
                            else:
                                st.error("❌ Erro na conexão SMTP. Verifique as configurações de email.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="align-center">', unsafe_allow_html=True)
                        st.markdown("### 📧 Envio em Massa")
                        st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço antes do botão
                        if st.button("📧 Enviar para Todos", type="primary", width='stretch'):
                            # Gerar newsletter
                            html_content = generate_html_newsletter(newsletter_title, st.session_state.news_items, newsletter_date, theme, compact_mode, layout_style)
                            text_content = generate_text_newsletter(newsletter_title, st.session_state.news_items, newsletter_date)
                            
                            # Confirmar envio
                            if st.checkbox("Confirma envio para todos os leads?"):
                                with st.spinner("Enviando newsletter..."):
                                    results = email_manager.send_newsletter(html_content, text_content, subscribed_leads, email_subject)
                                
                                # Mostrar resultados
                                st.success(f"✅ Newsletter enviada!")
                                st.info(f"**Resultados:** {results['sent']} enviados, {results['failed']} falharam")
                                
                                if results['errors']:
                                    st.error("❌ **Erros:**")
                                    for error in results['errors']:
                                        st.error(f"• {error}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown('<div class="align-right">', unsafe_allow_html=True)
                        st.markdown("### 🔄 Teste de Conexão")
                        st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço antes do botão
                        if st.button("🔄 Testar Conexão SMTP", type="secondary", width='stretch'):
                            if email_manager.test_connection():
                                st.success("✅ Conexão SMTP OK!")
                            else:
                                st.error("❌ Erro na conexão SMTP")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Espaçamento extra no final
                    st.markdown("<br><br><br>", unsafe_allow_html=True)
            else:
                st.error("❌ Erro ao conectar com Supabase")
