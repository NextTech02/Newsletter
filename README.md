# 📰 Newsletter FCP - Sistema Completo de Gerenciamento

Um sistema completo para criação, gerenciamento e envio de newsletters da **Federación Colombiana de Póker**, desenvolvido com Streamlit e integrado ao Supabase.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Supabase](https://img.shields.io/badge/Supabase-Integrado-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Visão Geral

Sistema profissional para criação e envio de newsletters com:
- **Editor visual** intuitivo
- **Gerenciamento de leads** com Supabase
- **Envio em massa** de emails
- **Temas personalizados** da FCP
- **Sistema de cancelamento** integrado
- **Otimização para Gmail** (evita corte de conteúdo)

## 🚀 Instalação Rápida

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/newsletter-fcp.git
cd newsletter-fcp
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Copie o arquivo de exemplo e configure suas credenciais:
```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
# Supabase Configuration
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase

# Email Configuration (Gmail)
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
SMTP_SERVER=your_smtp_server
SMTP_PORT=your_smpt_port
```

### 4. Execute a aplicação
```bash
streamlit run app.py
```

Acesse: `http://localhost:8501`

## 🗄️ Configuração do Supabase

### Criar a tabela de leads
```sql
CREATE TABLE leads_sem_duplicatas (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  nome VARCHAR(255),
  subscribed BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Configurar Gmail SMTP
1. Ative a **verificação em duas etapas** na sua conta Google
2. Gere uma **senha de app** específica
3. Use essa senha no campo `SMTP_PASSWORD`

## ✨ Funcionalidades

### 📝 Editor de Newsletter
- **Interface intuitiva** para criação de newsletters
- **Título personalizado** e múltiplas notícias
- **Preview em tempo real** com temas da FCP
- **Exportação** em HTML, Markdown e texto
- **Temas visuais** profissionais

### 👥 Gerenciamento de Leads
- **Integração completa** com Supabase
- **Paginação automática** (sem limite de 1000 registros)
- **Cache inteligente** para performance
- **Adicionar/visualizar** leads
- **Estatísticas** em tempo real
- **Filtros** e busca avançada

### 📤 Envio de Newsletter
- **Envio em massa** para todos os leads
- **Email de teste** antes do envio
- **Configuração SMTP** flexível
- **Relatórios** de entrega
- **Preview** antes do envio

### 🎨 Temas Disponíveis
- **Federación Poker** (padrão) - Design oficial da FCP
- **Claro** - Tema limpo e minimalista
- **Escuro** - Tema escuro elegante
- **Azul** - Tema corporativo azul
- **Verde** - Tema ecológico
- **Rosa** - Tema feminino

### 🔧 Recursos Avançados
- **Otimização para Gmail** (evita corte de conteúdo)
- **HTML compacto** para melhor entrega
- **Sistema de cancelamento** integrado
- **Design responsivo** para mobile
- **Logo FCP** integrada
- **Gradiente tricolor** (vermelho, amarelo, azul)

## 📁 Estrutura do Projeto

```
newsletter-fcp/
├── app.py                 # Aplicação principal
├── app_backup.py          # Backup da aplicação
├── config.py              # Configurações
├── email_manager.py       # Gerenciador de emails
├── supabase_manager.py    # Gerenciador do Supabase
├── requirements.txt       # Dependências Python
├── env.example           # Exemplo de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Este arquivo
└── logo1_fcp_branco.png  # Logo da FCP
```

## 🛠️ Tecnologias

- **Python 3.8+**
- **Streamlit** - Framework web
- **Supabase** - Backend como serviço
- **Pandas** - Manipulação de dados
- **SMTP** - Envio de emails
- **HTML/CSS** - Templates e estilos
- **JavaScript** - Interatividade

## 📊 Recursos de Performance

- **Cache inteligente** para leads
- **Paginação automática** no Supabase
- **HTML otimizado** para email
- **Compressão** de conteúdo
- **Indicadores de progresso** visuais

## 🔒 Segurança

- **Variáveis de ambiente** para credenciais
- **Validação de email** robusta
- **Sanitização** de dados
- **Conexão segura** SMTP

## 📱 Responsividade

- **Design mobile-first**
- **Templates responsivos**
- **Interface adaptável**
- **Testado em múltiplos dispositivos**

## 🚀 Deploy

### Heroku
```bash
# Criar Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Equipe

**Desenvolvedor:** José Felipe Pinto Faria

## 📞 Suporte

Para suporte, entre em contato:
- **Email:** jose.fpfaria@gmail.com

## 🎉 Agradecimentos

- **Streamlit** pela excelente framework
- **Supabase** pela infraestrutura robusta
- **Comunidade Python** pelo suporte

---

