# Etapa 1: Imagem base leve
FROM python:3.12-alpine

# Etapa 2: Labels (boas práticas OCI)
LABEL org.opencontainers.image.authors="Seu Nome"
LABEL org.opencontainers.image.title="Flask App Segura"
LABEL org.opencontainers.image.description="Aplicação Flask com boas práticas Docker"
LABEL org.opencontainers.image.version="1.0"

# Etapa 3: Criação de usuário não-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Etapa 4: Diretório de trabalho
WORKDIR /app

# Etapa 5: Copiar dependências e instalar
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del gcc musl-dev libffi-dev

# Etapa 6: Copiar aplicação
COPY app.py .

# Etapa 7: Usar usuário não-root
USER appuser

# Etapa 8: Expor porta
EXPOSE 80

# Etapa 9: Comando de execução
CMD ["python", "app.py"]

# Etapa 10: Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --spider http://localhost/health || exit 1