"""
FastAPI Application - Newsletter FCP
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Importar rotas
from app.routes import newsletter, leads, auth, users

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API para gerenciamento de Newsletter da Federación Colombiana de Póker"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Rota raiz - Health check"""
    return {
        "message": "Newsletter FCP API",
        "version": settings.API_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Incluir routers
app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_PREFIX}/users", tags=["users"])
app.include_router(newsletter.router, prefix=f"{settings.API_PREFIX}/newsletter", tags=["newsletter"])
app.include_router(leads.router, prefix=f"{settings.API_PREFIX}/leads", tags=["leads"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
