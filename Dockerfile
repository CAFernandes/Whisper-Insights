# ====================================
# Whisper-Insights - Dockerfile
# ====================================
# Multi-stage build para otimizar o tamanho da imagem final

# ====================================
# Stage 1: Builder (instalação de dependências)
# ====================================
FROM python:3.12-slim AS builder

# Definir argumentos de build
ARG DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema para compilação
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libssl-dev \
    libffi-dev \
    python3-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash whisper

# Configurar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (cache layer)
COPY requirements-docker.txt ./

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-docker.txt

# ====================================
# Stage 2: Runtime (imagem final)
# ====================================
FROM python:3.12-slim AS runtime

# Definir argumentos de build
ARG DEBIAN_FRONTEND=noninteractive

# Instalar dependências de runtime
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash whisper

# Copiar Python e dependências do builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Configurar diretório de trabalho
WORKDIR /app

# Copiar código da aplicação
COPY --chown=whisper:whisper . .

# Criar diretórios necessários
RUN mkdir -p uploads logs && \
    chown -R whisper:whisper /app

# Copiar e configurar entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir variáveis de ambiente
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Configurar porta
EXPOSE 5001

# Configurar volumes
VOLUME ["/app/uploads", "/app/logs"]

# Configurar health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Trocar para usuário não-root
USER whisper

# Definir entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "app.py"]