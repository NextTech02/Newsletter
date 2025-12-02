# 📰 Newsletter FCP - React + FastAPI

Sistema profissional de gerenciamento de Newsletter migrado para React + FastAPI.

## 🏗️ Arquitetura

```
Newsletter/
├── backend/               # API FastAPI
│   ├── app/
│   │   ├── main.py       # Aplicação principal
│   │   ├── config.py     # Configurações
│   │   ├── models/       # Schemas Pydantic
│   │   ├── routes/       # Endpoints da API
│   │   └── services/     # Lógica de negócio
│   └── requirements.txt
│
└── frontend/             # React + Material-UI
    ├── src/
    │   ├── components/   # Componentes React
    │   ├── pages/        # Páginas
    │   ├── services/     # API client
    │   └── main.jsx      # Entry point
    └── package.json
```

## 🚀 Configuração e Instalação

### 1. Backend (FastAPI)

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
copy .env.example .env
# Edite o .env com suas credenciais

# Executar servidor
python -m app.main
# ou
uvicorn app.main:app --reload
```

**Backend rodará em:** http://localhost:8000
**Documentação automática:** http://localhost:8000/docs

### 2. Frontend (React)

```bash
cd frontend

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev
```

**Frontend rodará em:** http://localhost:3000

## ⚙️ Configuração do Supabase

Configure as credenciais no arquivo `backend/.env`:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui
```

## 📧 Configuração de Email (SMTP)

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_app_google
```

## 🎯 Funcionalidades

### Dashboard
- Estatísticas em tempo real
- Visualização de métricas
- Cards informativos

### Gerenciamento de Leads
- Listar todos os leads
- Adicionar novos leads
- Remover leads
- Ver status de inscrição

### Editor de Newsletter
- Criar múltiplas notícias
- Preview em tempo real
- Envio de email de teste
- Envio em massa para todos os leads

## 📡 API Endpoints

### Leads
- `GET /api/v1/leads/` - Listar todos os leads
- `GET /api/v1/leads/subscribed` - Leads inscritos
- `POST /api/v1/leads/` - Criar lead
- `DELETE /api/v1/leads/{id}` - Deletar lead

### Newsletter
- `POST /api/v1/newsletter/preview` - Gerar preview
- `POST /api/v1/newsletter/send` - Enviar newsletter

## 🛠️ Tecnologias

**Backend:**
- FastAPI
- Python 3.8+
- Supabase
- Pydantic
- aiosmtplib

**Frontend:**
- React 18
- Material-UI (MUI)
- Axios
- React Router
- Vite

## 📦 Build para Produção

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
# Arquivos em: frontend/dist
```

## 🔒 Segurança

- Sem autenticação (conforme solicitado)
- CORS configurado
- Validação de dados com Pydantic
- Senhas de email em variáveis de ambiente

## 📞 Suporte

**Desenvolvido para:** Federación Colombiana de Póker
**Email:** jose.fpfaria@gmail.com

---

**© 2024 Federación Colombiana de Póker**
