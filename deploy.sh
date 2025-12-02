#!/bin/bash

# Script de Deploy para Newsletter FCP
# Execute: bash deploy.sh

set -e

echo "🚀 Iniciando deploy do Newsletter FCP..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se está na pasta correta
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}Erro: docker-compose.yml não encontrado!${NC}"
    echo "Execute este script na pasta raiz do projeto."
    exit 1
fi

# Parar containers existentes
echo -e "${YELLOW}Parando containers existentes...${NC}"
docker-compose down || true

# Remover imagens antigas
echo -e "${YELLOW}Removendo imagens antigas...${NC}"
docker system prune -f

# Build das imagens
echo -e "${YELLOW}Construindo imagens Docker...${NC}"
docker-compose build --no-cache

# Iniciar containers
echo -e "${YELLOW}Iniciando containers...${NC}"
docker-compose up -d

# Aguardar containers iniciarem
echo -e "${YELLOW}Aguardando containers iniciarem...${NC}"
sleep 10

# Verificar status
echo -e "${YELLOW}Verificando status dos containers...${NC}"
docker-compose ps

# Verificar logs
echo -e "${YELLOW}Últimas linhas dos logs:${NC}"
echo -e "${GREEN}=== Backend ===${NC}"
docker-compose logs --tail=20 backend

echo -e "${GREEN}=== Frontend ===${NC}"
docker-compose logs --tail=20 frontend

# Verificar saúde dos serviços
echo -e "${YELLOW}Testando endpoints...${NC}"
sleep 5

# Testar backend
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend está respondendo!${NC}"
else
    echo -e "${RED}✗ Backend não está respondendo${NC}"
fi

# Testar frontend
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend está respondendo!${NC}"
else
    echo -e "${RED}✗ Frontend não está respondendo${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Deploy concluído!${NC}"
echo ""
echo "Acesse:"
echo "  Frontend: http://seu-ip:3000"
echo "  Backend:  http://seu-ip:8000"
echo ""
echo "Para ver logs em tempo real:"
echo "  docker-compose logs -f"
echo ""
echo "Para parar os containers:"
echo "  docker-compose down"
