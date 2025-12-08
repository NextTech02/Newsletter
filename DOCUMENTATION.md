# Newsletter FCP - Documentação Completa

## Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Configuração do Ambiente de Desenvolvimento](#configuração-do-ambiente-de-desenvolvimento)
6. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
7. [Variáveis de Ambiente](#variáveis-de-ambiente)
8. [Executando Localmente](#executando-localmente)
9. [Build para Produção](#build-para-produção)
10. [Deploy em VPS (Hostinger + Cloudflare)](#deploy-em-vps-hostinger--cloudflare)
11. [Funcionalidades](#funcionalidades)
12. [API Endpoints](#api-endpoints)
13. [Troubleshooting](#troubleshooting)
14. [Manutenção e Atualizações](#manutenção-e-atualizações)

---

## Visão Geral

Sistema de gerenciamento de newsletters para a Federación Colombiana de Póker, permitindo:

- 📧 Criação e envio de newsletters personalizadas
- 👥 Gerenciamento de leads (inscritos)
- 🔐 Sistema de autenticação com JWT
- 👤 Gerenciamento de usuários administrativos
- 📊 Preview em tempo real das newsletters
- ✉️ Envio em massa com controle de taxa

### Características Principais

- **Frontend**: React + Vite + Material-UI
- **Backend**: FastAPI (Python)
- **Banco de Dados**: Supabase (PostgreSQL)
- **Email**: SMTP (Gmail)
- **Deploy**: Docker + Cloudflare Tunnel
- **SSL**: Automático via Cloudflare

---

## Arquitetura

```
┌─────────────────┐         ┌──────────────────┐
│   Cloudflare    │◄────────┤     Internet     │
│   (SSL + CDN)   │         │     (Users)      │
└────────┬────────┘         └──────────────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│  Cloudflare     │
│     Tunnel      │
│  (cloudflared)  │
└────────┬────────┘
         │
         │ HTTP (local)
         │
    ┌────┴─────────────────┐
    │                      │
┌───▼──────────┐    ┌──────▼────────┐
│   Frontend   │    │    Backend    │
│  (React)     │    │   (FastAPI)   │
│  Port: 8080  │    │  Port: 2052   │
└──────────────┘    └───────┬───────┘
                            │
                    ┌───────┴────────┐
                    │                │
            ┌───────▼──────┐  ┌──────▼──────┐
            │   Supabase   │  │    SMTP     │
            │ (PostgreSQL) │  │   (Gmail)   │
            └──────────────┘  └─────────────┘
```

### Fluxo de Dados

1. **Usuário** acessa `https://app.nexteventsco.com`
2. **Cloudflare** encripta (SSL) e roteia para o Cloudflare Tunnel
3. **Cloudflare Tunnel** encaminha para o container do frontend (porta 8080)
4. **Frontend** faz requisições para `https://api.nexteventsco.com`
5. **Cloudflare Tunnel** encaminha para o backend (porta 2052)
6. **Backend** processa e interage com Supabase e SMTP

---

## Tecnologias Utilizadas

### Backend

| Tecnologia | Versão | Propósito |
|-----------|--------|-----------|
| Python | 3.11 | Linguagem base |
| FastAPI | ≥0.104.0 | Framework web assíncrono |
| Uvicorn | ≥0.24.0 | Servidor ASGI |
| Supabase | ≥2.0.0 | Cliente para PostgreSQL |
| Pydantic | ≥2.0.0 | Validação de dados |
| Passlib | 1.7.4 | Hashing de senhas |
| bcrypt | 3.2.2 | Algoritmo de hash |
| python-jose | ≥3.3.0 | JWT tokens |
| aiosmtplib | ≥3.0.0 | Cliente SMTP assíncrono |
| Jinja2 | ≥3.1.2 | Templates HTML |

### Frontend

| Tecnologia | Versão | Propósito |
|-----------|--------|-----------|
| React | 18.x | Framework UI |
| Vite | 5.x | Build tool |
| Material-UI | 5.x | Componentes UI |
| Axios | 1.x | Cliente HTTP |
| React Router | 6.x | Roteamento |

### Infraestrutura

| Tecnologia | Propósito |
|-----------|-----------|
| Docker | Containerização |
| Docker Compose | Orquestração de containers |
| Nginx | Servidor web (frontend) |
| Cloudflare Tunnel | Proxy reverso + SSL |
| Cloudflare DNS | Gerenciamento de domínios |

---

## Estrutura do Projeto

```
Newsletter/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── schemas.py          # Modelos Pydantic
│   │   ├── routes/
│   │   │   ├── auth.py             # Endpoints de autenticação
│   │   │   ├── users.py            # Endpoints de usuários
│   │   │   ├── leads.py            # Endpoints de leads
│   │   │   └── newsletter.py       # Endpoints de newsletter
│   │   ├── services/
│   │   │   ├── auth_service.py     # Lógica de autenticação
│   │   │   ├── user_service.py     # Lógica de usuários
│   │   │   ├── supabase_service.py # Integração Supabase
│   │   │   ├── email_service.py    # Envio de emails
│   │   │   └── template_service.py # Geração de templates
│   │   ├── config.py               # Configurações
│   │   └── main.py                 # Entry point
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout.jsx          # Layout principal
│   │   │   └── PrivateRoute.jsx    # Proteção de rotas
│   │   ├── pages/
│   │   │   ├── Login.jsx           # Página de login
│   │   │   ├── Dashboard.jsx       # Dashboard
│   │   │   ├── Leads.jsx           # Gerenciamento de leads
│   │   │   ├── Newsletter.jsx      # Criação de newsletter
│   │   │   └── Users.jsx           # Gerenciamento de usuários
│   │   ├── services/
│   │   │   └── api.js              # Cliente API
│   │   ├── App.jsx                 # Componente raiz
│   │   └── main.jsx                # Entry point
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── .env.production
├── docker-compose.yml
├── .env
└── README.md
```

---

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- **Node.js** 20+ e npm
- **Python** 3.11+
- **Git**
- Conta no **Supabase**
- Conta no **Gmail** com App Password configurado

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/newsletter.git
cd newsletter
```

### 2. Configurar Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependências
npm install
```

---

## Configuração do Banco de Dados

### Criar Projeto no Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Crie uma nova organização
3. Crie um novo projeto
4. Anote a **URL** e **anon key**

### Criar Tabelas

Execute os seguintes SQLs no **SQL Editor** do Supabase:

#### Tabela: `newsletter_leads`

```sql
CREATE TABLE newsletter_leads (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  nome VARCHAR(255),
  subscribed BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_leads_email ON newsletter_leads(email);
CREATE INDEX idx_leads_subscribed ON newsletter_leads(subscribed);
```

#### Tabela: `users_newsletter`

```sql
CREATE TABLE users_newsletter (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_users_username ON users_newsletter(username);
CREATE INDEX idx_users_email ON users_newsletter(email);
```

### Criar Primeiro Usuário Administrador

```sql
-- Senha: admin123 (hash gerado com bcrypt)
INSERT INTO users_newsletter (username, email, password_hash)
VALUES (
  'admin',
  'admin@exemplo.com',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lE3PYqxqvK5u'
);
```

> ⚠️ **Importante**: Altere a senha após o primeiro login!

---

## Variáveis de Ambiente

### Backend (.env)

Crie o arquivo `backend/.env`:

```env
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-key

# SMTP (Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu-email@gmail.com
SMTP_PASSWORD=sua-app-password-do-gmail

# JWT
SECRET_KEY=gere-com-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# URLs
FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Tables
LEADS_TABLE=newsletter_leads
USERS_TABLE=users_newsletter
```

#### Como Obter App Password do Gmail

1. Acesse [myaccount.google.com](https://myaccount.google.com)
2. Vá em **Segurança** → **Verificação em duas etapas**
3. Ative a verificação em duas etapas
4. Vá em **Senhas de app**
5. Crie uma nova senha de app para "Outro"
6. Use essa senha no `SMTP_PASSWORD`

#### Gerar SECRET_KEY

```bash
openssl rand -hex 32
```

### Frontend (.env.production)

Crie o arquivo `frontend/.env.production`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

## Executando Localmente

### Backend

```bash
cd backend

# Ativar ambiente virtual
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Executar servidor
python -m app.main

# Ou com auto-reload:
uvicorn app.main:app --reload

# Servidor rodando em: http://localhost:8000
# Documentação interativa: http://localhost:8000/docs
```

### Frontend

```bash
cd frontend

# Executar servidor de desenvolvimento
npm run dev

# Frontend rodando em: http://localhost:5173
```

### Testar a Aplicação

1. Acesse http://localhost:5173
2. Faça login com:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Navegue pelas páginas:
   - **Dashboard**: Visualize estatísticas
   - **Leads**: Adicione/remova leads
   - **Newsletter**: Crie e envie newsletters
   - **Usuários**: Gerencie usuários administrativos

---

## Build para Produção

### Backend

O backend não requer build, apenas garantir que:
- Dependências estejam instaladas
- Variáveis de ambiente configuradas
- Servidor Uvicorn rodando

### Frontend

```bash
cd frontend

# Build de produção
npm run build

# Arquivos gerados em: frontend/dist/
```

O build do frontend gera arquivos estáticos otimizados que serão servidos pelo Nginx no Docker.

---

## Deploy em VPS (Hostinger + Cloudflare)

### Pré-requisitos

- VPS contratado na Hostinger
- Acesso SSH ao VPS
- Domínio registrado
- Conta no Cloudflare

### Etapa 1: Preparar o VPS

#### 1.1 Conectar via SSH

```bash
ssh root@IP_DO_VPS
```

#### 1.2 Atualizar Sistema

```bash
apt update && apt upgrade -y
```

#### 1.3 Instalar Docker

```bash
# Instalar Docker
curl -fsSL https://get.docker.com | sh

# Instalar Docker Compose
apt install docker-compose -y

# Verificar instalação
docker --version
docker-compose --version
```

#### 1.4 Instalar Git

```bash
apt install git -y
```

### Etapa 2: Clonar e Configurar Projeto

#### 2.1 Clonar Repositório

```bash
cd ~
mkdir -p var/www
cd var/www
git clone https://github.com/seu-usuario/newsletter.git
cd newsletter
```

#### 2.2 Configurar Variáveis de Ambiente

##### Arquivo Raiz (.env)

```bash
nano .env
```

Conteúdo:

```env
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-supabase

# SMTP Gmail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu-email@gmail.com
SMTP_PASSWORD=sua-app-password

# JWT
SECRET_KEY=sua-chave-secreta-64-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# URLs
FRONTEND_URL=https://app.nexteventsco.com

# Tables
LEADS_TABLE=newsletter_leads
USERS_TABLE=users_newsletter
```

##### Backend (.env)

```bash
nano backend/.env
```

Use o mesmo conteúdo acima.

##### Frontend (.env.production)

```bash
nano frontend/.env.production
```

Conteúdo:

```env
VITE_API_URL=https://api.nexteventsco.com/api/v1
```

> ⚠️ **Importante**:
> - Não use espaços ao redor do `=`
> - Não use aspas `"` ao redor dos valores
> - Não deixe espaços no final das linhas

#### 2.3 Verificar Arquivos

```bash
# Verificar .env (sem aspas e sem espaços)
cat -A .env

# Verificar backend/.env
cat -A backend/.env

# Verificar frontend/.env.production
cat frontend/.env.production
```

### Etapa 3: Configurar Cloudflare

#### 3.1 Adicionar Domínio ao Cloudflare

1. Acesse [dash.cloudflare.com](https://dash.cloudflare.com)
2. Clique em **"Add a Site"**
3. Digite seu domínio: `nexteventsco.com`
4. Escolha plano **FREE**
5. Cloudflare vai escanear seus registros DNS
6. **Anote os nameservers** fornecidos (ex: `drew.ns.cloudflare.com` e `rita.ns.cloudflare.com`)

#### 3.2 Alterar Nameservers na Hostinger

1. Acesse o painel da Hostinger
2. Vá em **Domínios** → Seu domínio
3. Procure por **Nameservers** ou **DNS**
4. Altere para os nameservers do Cloudflare
5. Salve as alterações

> ⏱️ **Nota**: A propagação pode levar de 5 minutos a 24 horas

#### 3.3 Verificar Propagação

```bash
# Na VPS, verificar DNS
nslookup api.nexteventsco.com
nslookup app.nexteventsco.com
```

Quando retornar os IPs corretos, a propagação está completa.

### Etapa 4: Instalar Cloudflare Tunnel

#### 4.1 Baixar cloudflared

```bash
cd ~
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

#### 4.2 Autenticar

```bash
cloudflared tunnel login
```

Isso vai abrir um link. Copie o link, abra no navegador e autorize.

#### 4.3 Criar Tunnel

```bash
cloudflared tunnel create newsletter-tunnel
```

Anote o **TUNNEL_ID** que aparece (ex: `77b9570a-0f56-409b-90f0-7ff5f67344cd`)

#### 4.4 Configurar Tunnel

```bash
sudo mkdir -p /etc/cloudflared
sudo nano /etc/cloudflared/config.yml
```

Conteúdo (substitua `TUNNEL_ID` pelo seu ID):

```yaml
tunnel: TUNNEL_ID
credentials-file: /root/.cloudflared/TUNNEL_ID.json

ingress:
  # Backend API
  - hostname: api.nexteventsco.com
    service: http://localhost:2052
  # Frontend App
  - hostname: app.nexteventsco.com
    service: http://localhost:8080
  # Catch-all (obrigatório)
  - service: http_status:404
```

#### 4.5 Configurar DNS no Cloudflare

##### Via Cloudflare Dashboard:

1. Acesse o painel do Cloudflare
2. Vá em **DNS** → **Records**
3. **Delete** os registros A existentes de `api` e `app` (se houver)
4. Adicione 2 registros **CNAME**:

**Registro 1 (Backend):**
- Type: `CNAME`
- Name: `api`
- Target: `TUNNEL_ID.cfargotunnel.com`
- Proxy status: **Proxied** (nuvem laranja)
- TTL: Auto

**Registro 2 (Frontend):**
- Type: `CNAME`
- Name: `app`
- Target: `TUNNEL_ID.cfargotunnel.com`
- Proxy status: **Proxied** (nuvem laranja)
- TTL: Auto

##### Ou via CLI:

```bash
cloudflared tunnel route dns TUNNEL_ID api.nexteventsco.com
cloudflared tunnel route dns TUNNEL_ID app.nexteventsco.com
```

#### 4.6 Instalar e Iniciar Serviço

```bash
# Instalar como serviço systemd
sudo cloudflared service install

# Iniciar serviço
sudo systemctl start cloudflared

# Habilitar inicialização automática
sudo systemctl enable cloudflared

# Verificar status
sudo systemctl status cloudflared
```

Deve aparecer **"active (running)"** e mensagens de **"Registered tunnel connection"**.

### Etapa 5: Deploy dos Containers

#### 5.1 Build e Iniciar Containers

```bash
cd ~/var/www/newsletter

# Build e iniciar
docker-compose up -d --build

# Verificar containers
docker-compose ps
```

Saída esperada:

```
NAME                  STATUS
newsletter-backend    Up (healthy)
newsletter-frontend   Up
```

#### 5.2 Verificar Logs

```bash
# Backend
docker logs newsletter-backend --tail 50

# Frontend
docker logs newsletter-frontend --tail 50

# Cloudflare Tunnel
sudo journalctl -u cloudflared -n 50 --no-pager
```

### Etapa 6: Configurar SSL no Cloudflare

1. Vá em **SSL/TLS** → **Overview**
2. Escolha: **Full** (recomendado)
   - **Flexible**: Cloudflare ↔ VPS sem SSL
   - **Full**: Cloudflare ↔ VPS com SSL auto-assinado
   - **Full (strict)**: Cloudflare ↔ VPS com SSL válido

### Etapa 7: Testar Deploy

#### 7.1 Testar Backend

```bash
curl https://api.nexteventsco.com/health
```

Deve retornar:

```json
{"status": "healthy"}
```

#### 7.2 Testar Frontend

Abra o navegador e acesse:

- **Frontend**: https://app.nexteventsco.com
- **Backend Docs**: https://api.nexteventsco.com/docs

#### 7.3 Testar Login

1. Acesse https://app.nexteventsco.com
2. Faça login com credenciais configuradas
3. Navegue pelas páginas

### Etapa 8: Configurações Adicionais (Opcional)

#### 8.1 Configurar Firewall

```bash
# Instalar UFW
apt install ufw -y

# Configurar regras
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp

# Ativar firewall
ufw enable

# Verificar status
ufw status
```

#### 8.2 Configurar Renovação Automática do Tunnel

O serviço systemd já faz isso automaticamente. Para verificar:

```bash
# Ver logs em tempo real
sudo journalctl -u cloudflared -f
```

---

## Funcionalidades

### 1. Autenticação

- **Login**: Sistema de autenticação com JWT
- **Proteção de Rotas**: Apenas usuários autenticados acessam o sistema
- **Tokens**: Expiração configurável (padrão 24h)
- **Logout**: Limpeza de tokens locais

### 2. Dashboard

- **Estatísticas**:
  - Total de leads
  - Leads inscritos
  - Total de usuários
- **Cards Visuais**: Interface com Material-UI
- **Navegação Rápida**: Links para outras páginas

### 3. Gerenciamento de Leads

- **Listar Leads**: Tabela com todos os leads
- **Adicionar Lead**: Formulário para novo lead (nome e email)
- **Remover Lead**: Botão de exclusão com confirmação
- **Status de Inscrição**: Visualização de leads inscritos/não inscritos
- **Busca e Filtros**: Pesquisa por email ou nome

### 4. Criação de Newsletter

- **Editor Multi-Notícia**: Adicione múltiplas notícias em uma newsletter
- **Campos por Notícia**:
  - Título
  - Conteúdo (texto rico)
- **Preview em Tempo Real**: Visualize o HTML gerado
- **Temas**: Personalização de cores
- **Envio**:
  - **Teste**: Envia apenas para o remetente
  - **Produção**: Envia para todos os leads inscritos
- **Controle de Taxa**: Envio em lotes de 50 emails com delay de 1s

### 5. Gerenciamento de Usuários

- **Listar Usuários**: Tabela com todos os usuários administrativos
- **Adicionar Usuário**: Criar novo usuário com:
  - Username
  - Email
  - Senha
- **Editar Usuário**: Atualizar informações
- **Deletar Usuário**: Remover usuário com confirmação
- **Status Ativo/Inativo**: Controle de acesso

---

## API Endpoints

### Autenticação

#### POST /api/v1/auth/login

Fazer login e obter token JWT.

**Request:**

```json
{
  "username": "admin",
  "password": "senha123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### POST /api/v1/auth/validate

Validar token JWT.

**Headers:**

```
Authorization: Bearer {token}
```

**Response:**

```json
{
  "valid": true,
  "username": "admin"
}
```

#### GET /api/v1/auth/me

Obter informações do usuário autenticado.

**Headers:**

```
Authorization: Bearer {token}
```

**Response:**

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@exemplo.com",
  "is_active": true
}
```

### Leads

#### GET /api/v1/leads/

Listar todos os leads.

**Response:**

```json
[
  {
    "id": 1,
    "email": "usuario@exemplo.com",
    "nome": "João Silva",
    "subscribed": true,
    "created_at": "2025-12-01T10:00:00Z"
  }
]
```

#### GET /api/v1/leads/subscribed

Listar apenas leads inscritos.

#### POST /api/v1/leads/

Criar novo lead.

**Request:**

```json
{
  "email": "novo@exemplo.com",
  "nome": "Novo Lead"
}
```

#### DELETE /api/v1/leads/{lead_id}

Deletar lead por ID.

#### POST /api/v1/leads/unsubscribe?email={email}

Cancelar inscrição de um lead.

### Newsletter

#### POST /api/v1/newsletter/preview

Gerar preview da newsletter.

**Request:**

```json
{
  "subject": "Newsletter de Dezembro",
  "news_items": [
    {
      "title": "Título da Notícia",
      "content": "Conteúdo da notícia..."
    }
  ],
  "theme": {
    "primary_color": "#FF4B4B",
    "secondary_color": "#FFD700"
  }
}
```

**Response:**

```json
{
  "html": "<html>...</html>"
}
```

#### POST /api/v1/newsletter/send

Enviar newsletter.

**Request:**

```json
{
  "subject": "Newsletter de Dezembro",
  "news_items": [
    {
      "title": "Título da Notícia",
      "content": "Conteúdo..."
    }
  ],
  "theme": {
    "primary_color": "#FF4B4B"
  },
  "is_test": false
}
```

**Response:**

```json
{
  "message": "Newsletter enviada com sucesso",
  "sent_count": 150,
  "failed_count": 0
}
```

### Usuários

#### GET /api/v1/users/

Listar todos os usuários.

#### POST /api/v1/users/

Criar novo usuário.

**Request:**

```json
{
  "username": "novousuario",
  "email": "novo@exemplo.com",
  "password": "senha123"
}
```

#### GET /api/v1/users/{user_id}

Obter usuário por ID.

#### PUT /api/v1/users/{user_id}

Atualizar usuário.

#### DELETE /api/v1/users/{user_id}

Deletar usuário.

---

## Troubleshooting

### Problema: Login não funciona (401 Unauthorized)

**Possíveis Causas:**

1. Credenciais incorretas
2. Usuário não existe no banco
3. Senha hash incorreta no banco

**Solução:**

```bash
# Verificar logs do backend
docker logs newsletter-backend --tail 50

# Testar diretamente na API
curl -X POST http://localhost:2052/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"senha123"}'

# Verificar usuário no Supabase
# Acesse o SQL Editor e execute:
SELECT * FROM users_newsletter WHERE username = 'admin';
```

### Problema: Erro de CORS

**Sintoma:**

```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Solução:**

1. Verificar `CORS_ORIGINS` no backend:

```bash
docker exec newsletter-backend printenv | grep CORS
```

Deve incluir: `https://app.nexteventsco.com`

2. Verificar configuração no `backend/app/config.py`:

```python
CORS_ORIGINS: Union[list, str] = [
  "http://localhost:3000",
  "http://localhost:5173",
  "https://app.nexteventsco.com"
]
```

3. Reiniciar backend:

```bash
docker-compose restart backend
```

### Problema: Erro de bcrypt (password longer than 72 bytes)

**Sintoma:**

```
ValueError: password cannot be longer than 72 bytes
```

**Solução:**

1. Verificar versão do bcrypt:

```bash
docker exec newsletter-backend pip show bcrypt
```

Deve ser **3.2.2** (não 4.x ou 5.x)

2. Corrigir `requirements.txt`:

```txt
passlib[bcrypt]==1.7.4
bcrypt==3.2.2
```

3. Rebuild:

```bash
docker-compose down
docker rmi newsletter-backend -f
docker-compose build --no-cache backend
docker-compose up -d
```

### Problema: Frontend tentando acessar localhost

**Sintoma:**

```
POST http://localhost:8000/api/v1/auth/login net::ERR_FAILED
```

**Solução:**

1. Verificar `.env.production`:

```bash
cat frontend/.env.production
```

Deve ter:

```env
VITE_API_URL=https://api.nexteventsco.com/api/v1
```

2. Rebuild do frontend:

```bash
docker-compose down
docker rmi newsletter-frontend -f
docker-compose build --no-cache frontend
docker-compose up -d
```

3. Limpar cache do navegador (Ctrl+Shift+Del)

### Problema: Erro ao enviar email

**Sintomas:**

- SMTPAuthenticationError
- Connection refused
- Timeout

**Solução:**

1. Verificar credenciais SMTP:

```bash
docker exec newsletter-backend printenv | grep SMTP
```

2. Verificar se é **App Password** do Gmail (não senha normal)

3. Testar conexão SMTP:

```bash
# Instalar ferramenta de teste
apt install swaks -y

# Testar SMTP
swaks --to destino@exemplo.com \
  --from seu-email@gmail.com \
  --server smtp.gmail.com:587 \
  --auth LOGIN \
  --auth-user seu-email@gmail.com \
  --auth-password sua-app-password \
  --tls
```

4. Verificar se tem aspas ou espaços no `.env`:

```bash
cat -A .env | grep SMTP_PASSWORD
```

Não deve ter `"` ou espaços extras.

### Problema: Cloudflare Tunnel não conecta

**Sintoma:**

```
failed to dial to edge with quic: timeout
```

**Solução:**

1. Verificar se o serviço está rodando:

```bash
sudo systemctl status cloudflared
```

2. Reiniciar serviço:

```bash
sudo systemctl restart cloudflared
```

3. Verificar configuração:

```bash
cat /etc/cloudflared/config.yml
```

4. Verificar logs:

```bash
sudo journalctl -u cloudflared -n 50 --no-pager
```

5. Verificar DNS no Cloudflare:

- Os CNAMEs estão criados?
- Estão apontando para `TUNNEL_ID.cfargotunnel.com`?
- Proxy está ativado (nuvem laranja)?

### Problema: Container com status "unhealthy"

**Solução:**

1. Verificar healthcheck:

```bash
docker inspect newsletter-backend | grep -A 10 Health
```

2. Testar endpoint de health:

```bash
curl http://localhost:2052/health
```

3. Ver logs:

```bash
docker logs newsletter-backend --tail 50
```

### Problema: Variáveis de ambiente não carregam

**Sintoma:**

Valores antigos persistem mesmo após editar `.env`

**Solução:**

1. **Reiniciar não basta** - precisa recriar:

```bash
docker-compose down
docker-compose up -d
```

2. Verificar se não há espaços ou aspas:

```bash
cat -A .env
cat -A backend/.env
```

3. Verificar se há múltiplos `.env`:

```bash
find ~/var/www/newsletter -name ".env" -type f
```

---

## Manutenção e Atualizações

### Atualizar Código

```bash
cd ~/var/www/newsletter

# Fazer backup do .env
cp .env .env.backup
cp backend/.env backend/.env.backup

# Puxar atualizações
git pull origin main

# Rebuild e reiniciar
docker-compose down
docker-compose up -d --build

# Verificar
docker-compose ps
docker logs newsletter-backend --tail 20
docker logs newsletter-frontend --tail 20
```

### Backup do Banco de Dados

O Supabase faz backup automático, mas você pode exportar manualmente:

1. Acesse o painel do Supabase
2. Vá em **Database** → **Backups**
3. Clique em **Download Backup**

Ou via SQL:

```bash
# Instalar cliente PostgreSQL
apt install postgresql-client -y

# Fazer dump
pg_dump -h db.seu-projeto.supabase.co \
  -U postgres \
  -d postgres \
  --no-owner \
  --no-acl \
  > backup_$(date +%Y%m%d).sql
```

### Monitoramento

#### Verificar Status dos Containers

```bash
# Status geral
docker-compose ps

# Uso de recursos
docker stats newsletter-backend newsletter-frontend

# Logs em tempo real
docker-compose logs -f
```

#### Verificar Cloudflare Tunnel

```bash
# Status do serviço
sudo systemctl status cloudflared

# Logs em tempo real
sudo journalctl -u cloudflared -f
```

#### Verificar Disco

```bash
# Espaço em disco
df -h

# Limpar containers e imagens antigas
docker system prune -a -f
```

### Reiniciar Serviços

```bash
# Reiniciar apenas backend
docker-compose restart backend

# Reiniciar apenas frontend
docker-compose restart frontend

# Reiniciar Cloudflare Tunnel
sudo systemctl restart cloudflared

# Reiniciar tudo
docker-compose restart
```

### Logs Importantes

```bash
# Backend (últimas 100 linhas)
docker logs newsletter-backend --tail 100

# Frontend (últimas 100 linhas)
docker logs newsletter-frontend --tail 100

# Cloudflare Tunnel (últimas 100 linhas)
sudo journalctl -u cloudflared -n 100 --no-pager

# Seguir logs em tempo real (todos)
docker-compose logs -f &
sudo journalctl -u cloudflared -f
```

### Renovar Certificados SSL

**Não é necessário!** O Cloudflare gerencia os certificados automaticamente.

### Escalar Aplicação

#### Aumentar Recursos do Container

Edite `docker-compose.yml`:

```yaml
services:
  backend:
    # ... outras configurações
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

Aplique:

```bash
docker-compose up -d
```

---

## Segurança

### Boas Práticas

1. **Nunca commitar arquivos .env no Git**
   - Adicione ao `.gitignore`

2. **Usar senhas fortes**
   - Especialmente `SECRET_KEY`
   - Gerar com `openssl rand -hex 32`

3. **Atualizar regularmente**
   - Dependências do Python: `pip list --outdated`
   - Dependências do Node: `npm outdated`

4. **Firewall configurado**
   - Apenas portas necessárias abertas

5. **Backup regular**
   - Banco de dados (Supabase faz automático)
   - Código (Git)
   - Configurações (.env)

6. **Monitorar logs**
   - Ataques de força bruta no login
   - Erros inesperados
   - Uso anormal de recursos

### Hardening Adicional

#### Limitar Tentativas de Login

Adicione rate limiting no backend (já implementado com FastAPI).

#### HTTPS Obrigatório

Cloudflare já força HTTPS automaticamente.

#### Headers de Segurança

Adicione no `nginx.conf` (frontend):

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

---

## Contato e Suporte

### Repositório

- **GitHub**: https://github.com/seu-usuario/newsletter

### Documentação Adicional

- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **Supabase**: https://supabase.com/docs
- **Cloudflare Tunnel**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps
- **Docker**: https://docs.docker.com

### Logs de Alterações

Mantenha um CHANGELOG.md com:

- Versões
- Data de release
- Novas funcionalidades
- Correções de bugs
- Breaking changes

---

## Glossário

- **VPS**: Virtual Private Server - Servidor virtual privado
- **JWT**: JSON Web Token - Token de autenticação
- **CORS**: Cross-Origin Resource Sharing - Compartilhamento de recursos entre origens
- **SMTP**: Simple Mail Transfer Protocol - Protocolo de envio de emails
- **SSL/TLS**: Secure Sockets Layer / Transport Layer Security - Criptografia
- **CDN**: Content Delivery Network - Rede de distribuição de conteúdo
- **DNS**: Domain Name System - Sistema de nomes de domínio
- **API**: Application Programming Interface - Interface de programação
- **REST**: Representational State Transfer - Arquitetura de API
- **Tunnel**: Túnel criptografado para tráfego HTTP/HTTPS

---

## Apêndice A: Comandos Úteis

### Docker

```bash
# Ver todos os containers
docker ps -a

# Parar todos os containers
docker stop $(docker ps -q)

# Remover todos os containers
docker rm $(docker ps -aq)

# Remover todas as imagens
docker rmi $(docker images -q)

# Limpar tudo
docker system prune -a -f --volumes

# Ver logs de um container
docker logs -f CONTAINER_NAME

# Entrar em um container
docker exec -it CONTAINER_NAME /bin/sh

# Ver uso de recursos
docker stats
```

### Docker Compose

```bash
# Iniciar
docker-compose up -d

# Parar
docker-compose down

# Rebuild
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend

# Reiniciar um serviço
docker-compose restart backend

# Escalar serviço
docker-compose up -d --scale backend=3
```

### Git

```bash
# Ver status
git status

# Adicionar arquivos
git add .

# Commit
git commit -m "Mensagem"

# Push
git push origin main

# Pull
git pull origin main

# Ver histórico
git log --oneline

# Criar branch
git checkout -b feature/nova-funcionalidade

# Desfazer mudanças não commitadas
git checkout -- .
```

### Systemctl (Cloudflare Tunnel)

```bash
# Ver status
sudo systemctl status cloudflared

# Iniciar
sudo systemctl start cloudflared

# Parar
sudo systemctl stop cloudflared

# Reiniciar
sudo systemctl restart cloudflared

# Habilitar auto-start
sudo systemctl enable cloudflared

# Desabilitar auto-start
sudo systemctl disable cloudflared

# Ver logs
sudo journalctl -u cloudflared -f
```

---

## Apêndice B: Estrutura de Dados

### Modelo: Lead

```python
{
  "id": int,
  "email": str,
  "nome": str | null,
  "subscribed": bool,
  "created_at": datetime
}
```

### Modelo: User

```python
{
  "id": int,
  "username": str,
  "email": str,
  "password_hash": str,
  "is_active": bool,
  "created_at": datetime
}
```

### Modelo: Newsletter

```python
{
  "subject": str,
  "news_items": [
    {
      "title": str,
      "content": str
    }
  ],
  "theme": {
    "primary_color": str,
    "secondary_color": str,
    "tertiary_color": str
  },
  "is_test": bool
}
```

---

## Apêndice C: Portas Utilizadas

| Serviço | Porta Interna | Porta Externa | Protocolo |
|---------|---------------|---------------|-----------|
| Backend (container) | 8000 | 2052 | HTTP |
| Frontend (container) | 80 | 8080 | HTTP |
| Cloudflare Tunnel | - | - | HTTPS |
| PostgreSQL (Supabase) | 5432 | - | TCP |
| SMTP (Gmail) | 587 | - | TLS |

---

## Apêndice D: Checklist de Deploy

- [ ] VPS provisionado e acessível via SSH
- [ ] Docker e Docker Compose instalados
- [ ] Git instalado
- [ ] Projeto clonado na VPS
- [ ] Arquivo `.env` na raiz configurado corretamente
- [ ] Arquivo `backend/.env` configurado corretamente
- [ ] Arquivo `frontend/.env.production` configurado corretamente
- [ ] Domínio adicionado ao Cloudflare
- [ ] Nameservers alterados na Hostinger
- [ ] DNS propagado (testado com `nslookup`)
- [ ] Cloudflare Tunnel instalado (`cloudflared`)
- [ ] Tunnel autenticado e criado
- [ ] Arquivo `/etc/cloudflared/config.yml` configurado
- [ ] CNAMEs criados no Cloudflare (`api` e `app`)
- [ ] Serviço `cloudflared` rodando e conectado
- [ ] Containers buildados e rodando (`docker-compose ps`)
- [ ] Backend acessível via `https://api.nexteventsco.com/health`
- [ ] Frontend acessível via `https://app.nexteventsco.com`
- [ ] Login funcionando
- [ ] SMTP testado e emails enviando
- [ ] Tabelas criadas no Supabase
- [ ] Usuário administrador criado
- [ ] Firewall configurado (UFW)
- [ ] Backup configurado

---

**Documentação criada em**: 03/12/2025
**Versão**: 1.0.0
**Última atualização**: 03/12/2025

---

