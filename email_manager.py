import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import get_email_config
from typing import List, Dict
import time

class EmailManager:
    def __init__(self):
        self.config = get_email_config()
    
    def send_newsletter(self, newsletter_html: str, newsletter_text: str, recipients: List[Dict], subject: str = "Newsletter") -> Dict:
        """Envia newsletter para uma lista de recipients"""
        results = {
            'sent': 0,
            'failed': 0,
            'errors': []
        }
        
        if not self.config['smtp_username'] or not self.config['smtp_password']:
            st.warning("⚠️ Configurações de email não encontradas. Configure SMTP_USERNAME e SMTP_PASSWORD nas variáveis de ambiente.")
            return results
        
        try:
            # Conectar ao servidor SMTP
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['smtp_username'], self.config['smtp_password'])
            
            # Enviar para cada recipient
            for recipient in recipients:
                try:
                    # Criar mensagem para cada recipient - FORÇAR HTML
                    msg = MIMEMultipart('related')
                    msg['From'] = self.config['smtp_username']
                    msg['To'] = recipient['email']
                    msg['Subject'] = subject
                    msg['MIME-Version'] = '1.0'
                    msg['Content-Type'] = 'text/html; charset=utf-8'
                    
                    # Adicionar apenas versão HTML (forçar renderização)
                    html_part = MIMEText(newsletter_html, 'html', 'utf-8')
                    html_part.add_header('Content-Type', 'text/html; charset=utf-8')
                    html_part.add_header('Content-Disposition', 'inline')
                    
                    # Anexar apenas HTML
                    msg.attach(html_part)
                    
                    # Enviar mensagem
                    server.send_message(msg)
                    results['sent'] += 1
                    time.sleep(0.1)  # Pequena pausa entre envios
                    
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append(f"Erro ao enviar para {recipient['email']}: {str(e)}")
            
            server.quit()
            
        except Exception as e:
            results['errors'].append(f"Erro geral de envio: {str(e)}")
            st.error(f"Erro ao enviar newsletter: {str(e)}")
        
        return results
    
    def test_connection(self) -> bool:
        """Testa a conexão SMTP"""
        try:
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['smtp_username'], self.config['smtp_password'])
            server.quit()
            return True
        except Exception as e:
            st.error(f"Erro na conexão SMTP: {str(e)}")
            return False
