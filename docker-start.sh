#!/bin/bash
# ====================================
# Whisper-Insights - Docker Start Script
# ====================================

set -e

echo "🐳 Whisper-Insights - Docker Startup"
echo "===================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado!"
    echo "📖 Instale o Docker em: https://docs.docker.com/install/"
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado!"
    echo "📖 Instale o Docker Compose em: https://docs.docker.com/compose/install/"
    exit 1
fi

# Verificar se Docker está rodando
if ! docker info &> /dev/null; then
    echo "❌ Docker não está rodando!"
    echo "🚀 Inicie o Docker e tente novamente"
    exit 1
fi

echo "✅ Docker verificado"

# Verificar arquivo .env
if [ ! -f ".env" ]; then
    echo "⚠️ Arquivo .env não encontrado"
    if [ -f ".env.example" ]; then
        echo "📝 Criando .env a partir do .env.example..."
        cp .env.example .env
        echo "✅ .env criado!"
        echo "🔧 Edite o arquivo .env conforme necessário"
    else
        echo "❌ .env.example não encontrado!"
        exit 1
    fi
fi

# Verificar modo de execução
MODE=${1:-dev}

case $MODE in
    "dev"|"development")
        echo "🔧 Iniciando em modo desenvolvimento..."
        docker-compose up --build
        ;;
    "prod"|"production")
        echo "🏭 Iniciando em modo produção..."
        docker-compose --profile production up -d --build
        echo "✅ Serviços iniciados em background"
        echo "🌐 Aplicação: http://localhost"
        echo "📋 Logs: docker-compose logs -f"
        ;;
    "init")
        echo "🎬 Configuração inicial..."
        make init
        ;;
    *)
        echo "❓ Modo inválido: $MODE"
        echo "📖 Uso: $0 [dev|prod|init]"
        echo "   dev  - Modo desenvolvimento (padrão)"
        echo "   prod - Modo produção com Nginx"
        echo "   init - Configuração inicial completa"
        exit 1
        ;;
esac
