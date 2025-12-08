# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Newsletter management system for Federación Colombiana de Póker built with React (frontend) and FastAPI (backend). The system includes JWT authentication, user management, lead tracking, and newsletter creation with bulk email sending capabilities.

## Development Commands

### Backend (FastAPI)

```bash
# Setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows (or: source venv/bin/activate on Linux/Mac)
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run development server
python -m app.main
# or with auto-reload
uvicorn app.main:app --reload

# Backend runs at: http://localhost:8000
# Auto-generated API docs: http://localhost:8000/docs
# Health check: http://localhost:8000/health
```

### Frontend (React + Vite)

```bash
# Setup
cd frontend
npm install

# Run development server
npm run dev
# Frontend runs at: http://localhost:5173

# Build for production
npm run build
# Output: frontend/dist

# Preview production build
npm run preview
```

### Docker (Production)

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker logs newsletter-backend --tail 50
docker logs newsletter-frontend --tail 50

# Check container status
docker-compose ps

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart backend
```

## Architecture

### Backend Structure

**Service Layer Pattern**: Business logic is separated into dedicated services:
- `auth_service.py`: JWT authentication and password hashing with bcrypt
- `user_service.py`: User management operations
- `supabase_service.py`: Database operations with automatic pagination (1000 records/page)
- `email_service.py`: SMTP email sending with async batch processing (50 emails/batch)
- `template_service.py`: HTML newsletter generation with embedded styles

**Key Services**:
- **AuthService** (backend/app/services/auth_service.py): Handles JWT token generation, validation, and password hashing using passlib with bcrypt.
- **UserService** (backend/app/services/user_service.py): Manages user CRUD operations. Stores password hashes in Supabase `users_newsletter` table.
- **SupabaseService** (backend/app/services/supabase_service.py): Handles all database operations. Uses pagination for large datasets. Methods return Dict/List[Dict] to avoid SQLAlchemy dependencies.
- **EmailService** (backend/app/services/email_service.py): Async email sending via aiosmtplib. `send_bulk_emails()` processes in batches with 1-second delays between batches to avoid rate limiting.
- **TemplateService** (backend/app/services/template_service.py): Generates newsletter HTML with inline styles for email compatibility. Theme colors: primary=#FF4B4B, secondary=#FFD700, tertiary=#4169E1.

**Configuration**: All settings in `backend/app/config.py` using Pydantic settings management. Environment variables loaded from `.env` file.

**Data Models** (backend/app/models/schemas.py):
- Pydantic models for validation
- `UserCreate/UserResponse`: User authentication and management
- `Token/TokenData`: JWT authentication tokens
- `NewsItem`: Individual news article with title and content
- `NewsletterCreate`: Newsletter with subject, list of news items, and theme
- `EmailSendRequest`: Supports test mode (sends to sender only) and bulk mode (sends to all subscribed leads)

### Frontend Structure

**React + Material-UI**: Single-page application with React Router v6.

**Pages**:
- `Login.jsx`: JWT authentication with token storage
- `Dashboard.jsx`: Stats cards and metrics overview (protected route)
- `Leads.jsx`: Lead management (add/remove leads)
- `Newsletter.jsx`: Multi-news editor with preview and send functionality
- `Users.jsx`: Admin user management
- `Unsubscribe.jsx`: Public unsubscribe form with multilingual support (PT/ES)

**Components**:
- `Layout.jsx`: Main application layout with navigation
- `PrivateRoute.jsx`: Route protection wrapper for authenticated pages

**API Client** (frontend/src/services/api.js):
- Axios-based client with base URL configured via environment variable
- JWT token automatically added to request headers
- Organized into `authAPI`, `leadsAPI`, `newsletterAPI`, and `usersAPI` namespaces

### Data Flow

1. **Authentication**: User logs in at `Login.jsx` → POST `/api/v1/auth/login` → `auth_service` validates credentials → JWT token returned and stored in localStorage → token added to all subsequent API requests via axios interceptor
2. **Newsletter Creation**: User creates newsletter in `Newsletter.jsx` → calls `/api/v1/newsletter/preview` → `template_service` generates HTML → preview shown
3. **Newsletter Sending**: User clicks send → calls `/api/v1/newsletter/send` → `supabase_service` fetches subscribed leads → `email_service` sends in batches → returns success/failure counts
4. **Lead Management**: CRUD operations through `/api/v1/leads/*` → `supabase_service` interacts with Supabase table `newsletter_leads`
5. **User Management**: Admin operations through `/api/v1/users/*` → `user_service` manages users in `users_newsletter` table
6. **Unsubscribe**: User fills form at `Unsubscribe.jsx` → POST `/api/v1/leads/unsubscribe` with email, reason, and comments → `supabase_service` verifies email exists → deletes lead from database → returns success message

## Environment Configuration

Backend requires `.env` file in `backend/` directory:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# SMTP (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# JWT Authentication
SECRET_KEY=generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Table Names
LEADS_TABLE=newsletter_leads
USERS_TABLE=users_newsletter
```

Frontend requires `.env.production` file in `frontend/` directory for production:

```env
VITE_API_URL=https://api.nexteventsco.com/api/v1
```

**Important**: Generate SECRET_KEY using: `openssl rand -hex 32`

## Database Schema

### Table: `newsletter_leads`
- `id`: BIGSERIAL PRIMARY KEY
- `email`: VARCHAR(255) NOT NULL UNIQUE
- `nome`: VARCHAR(255)
- `subscribed`: BOOLEAN DEFAULT true
- `created_at`: TIMESTAMP WITH TIME ZONE DEFAULT NOW()

### Table: `users_newsletter`
- `id`: BIGSERIAL PRIMARY KEY
- `username`: VARCHAR(100) NOT NULL UNIQUE
- `email`: VARCHAR(255) NOT NULL UNIQUE
- `password_hash`: VARCHAR(255) NOT NULL (bcrypt hashed)
- `is_active`: BOOLEAN DEFAULT true
- `created_at`: TIMESTAMP WITH TIME ZONE DEFAULT NOW()

Note: The service checks if `subscribed` column exists at runtime and falls back to returning all leads if it doesn't.

## Key Behavioral Notes

- **JWT Authentication**: System uses JWT tokens for authentication with 24-hour expiration (configurable)
- **Password Security**: Passwords hashed using bcrypt via passlib. Important: Use bcrypt version compatible with passlib (avoid bcrypt 4.x+ which has breaking changes)
- **Protected Routes**: Frontend uses `PrivateRoute` component to protect authenticated pages
- **CORS**: Backend configured to allow localhost:3000, localhost:5173, and production domain
- **Email Batching**: Bulk sends process 50 emails at a time with 1-second pauses to avoid rate limits
- **Test Mode**: Newsletter send supports `is_test=true` which sends only to SMTP_USERNAME for testing
- **Pagination Handling**: Supabase queries automatically paginate through large result sets in 1000-record chunks
- **Unsubscribe**: Public endpoint that deletes the lead record entirely from the database. Accepts email, reason (required), and optional comments. No authentication required for this endpoint

## Deployment

The application is deployed using Docker with Cloudflare Tunnel for SSL termination:
- **Backend**: Runs on port 2052 (mapped from container port 8000)
- **Frontend**: Runs on port 8080 (mapped from container port 80, served by Nginx)
- **Cloudflare Tunnel**: Provides HTTPS termination and routes traffic to local ports
- **Production URLs**:
  - Frontend: https://app.nexteventsco.com
  - Backend API: https://api.nexteventsco.com

See `DOCUMENTATION.md` for detailed deployment instructions.
