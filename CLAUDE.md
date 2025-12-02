# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Newsletter management system for Federación Colombiana de Póker built with React (frontend) and FastAPI (backend). The system allows creating and sending newsletters to subscribed leads with email tracking, HTML templating, and bulk sending capabilities.

## Development Commands

### Backend (FastAPI)

```bash
# Setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run development server
python -m app.main
# or with auto-reload
uvicorn app.main:app --reload

# Backend runs at: http://localhost:8000
# Auto-generated API docs: http://localhost:8000/docs
```

### Frontend (React + Vite)

```bash
# Setup
cd frontend
npm install

# Run development server
npm run dev
# Frontend runs at: http://localhost:3000 or http://localhost:5173

# Build for production
npm run build
# Output: frontend/dist
```

## Architecture

### Backend Structure

**Service Layer Pattern**: Business logic is separated into dedicated services:
- `supabase_service.py`: Database operations with automatic pagination (1000 records/page)
- `email_service.py`: SMTP email sending with async batch processing (50 emails/batch)
- `template_service.py`: HTML newsletter generation with embedded styles

**Key Services**:
- **SupabaseService** (backend/app/services/supabase_service.py): Handles all database operations. Uses pagination for large datasets. Methods return Dict/List[Dict] to avoid SQLAlchemy dependencies.
- **EmailService** (backend/app/services/email_service.py): Async email sending via aiosmtplib. `send_bulk_emails()` processes in batches with 1-second delays between batches to avoid rate limiting.
- **TemplateService** (backend/app/services/template_service.py): Generates newsletter HTML with inline styles for email compatibility. Theme colors: primary=#FF4B4B, secondary=#FFD700, tertiary=#4169E1.

**Configuration**: All settings in `backend/app/config.py` using Pydantic settings management. Environment variables loaded from `.env` file.

**Data Models** (backend/app/models/schemas.py):
- Pydantic models for validation
- `NewsItem`: Individual news article with title and content
- `NewsletterCreate`: Newsletter with subject, list of news items, and theme
- `EmailSendRequest`: Supports test mode (sends to sender only) and bulk mode (sends to all subscribed leads)

### Frontend Structure

**React + Material-UI**: Single-page application with React Router v6.

**Pages**:
- `Dashboard.jsx`: Stats cards and metrics overview
- `Leads.jsx`: Lead management (add/remove leads)
- `Newsletter.jsx`: Multi-news editor with preview and send functionality

**API Client** (frontend/src/services/api.js):
- Axios-based client with base URL http://localhost:8000/api/v1
- Organized into `leadsAPI` and `newsletterAPI` namespaces

### Data Flow

1. **Newsletter Creation**: User creates newsletter in `Newsletter.jsx` → calls `/api/v1/newsletter/preview` → `template_service` generates HTML → preview shown
2. **Newsletter Sending**: User clicks send → calls `/api/v1/newsletter/send` → `supabase_service` fetches subscribed leads → `email_service` sends in batches → returns success/failure counts
3. **Lead Management**: CRUD operations through `/api/v1/leads/*` → `supabase_service` interacts with Supabase table `newsletter_leads`

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
```

## Database Schema

Supabase table: `newsletter_leads`
- `id`: Primary key (int)
- `email`: Email address (required)
- `nome`: Name (optional)
- `subscribed`: Boolean flag (optional, defaults to true if column exists)
- `created_at`: Timestamp (optional)

Note: The service checks if `subscribed` column exists at runtime and falls back to returning all leads if it doesn't.

## Key Behavioral Notes

- **No Authentication**: System operates without user authentication as requested
- **CORS**: Backend configured to allow localhost:3000 and localhost:5173
- **Email Batching**: Bulk sends process 50 emails at a time with 1-second pauses to avoid rate limits
- **Test Mode**: Newsletter send supports `is_test=true` which sends only to SMTP_USERNAME for testing
- **Pagination Handling**: Supabase queries automatically paginate through large result sets in 1000-record chunks
- **Unsubscribe**: Currently deletes the lead record entirely (not just updating a flag)
