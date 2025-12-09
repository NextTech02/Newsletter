  # Multi-stage build para Frontend React
  FROM node:20-alpine AS builder

  # Argumentos de build
  ARG VITE_API_URL

  # Configurar diretório de trabalho
  WORKDIR /app

  # Copiar package files
  COPY package*.json ./

  # Instalar dependências
  RUN npm ci

  # Copiar código fonte
  COPY . .

  # Passar variável de ambiente para o build
  ENV VITE_API_URL=$VITE_API_URL

  # Build da aplicação
  RUN npm run build

  # Debug: mostrar a URL que foi usada
  RUN echo "Build completed with VITE_API_URL=$VITE_API_URL"

  # Stage 2: Servir com Nginx
  FROM nginx:alpine

  # Copiar build do stage anterior
  COPY --from=builder /app/dist /usr/share/nginx/html

  # Copiar configuração customizada do Nginx
  COPY nginx.conf /etc/nginx/conf.d/default.conf

  # Expor porta
  EXPOSE 80

  # Iniciar Nginx
  CMD ["nginx", "-g", "daemon off;"]
