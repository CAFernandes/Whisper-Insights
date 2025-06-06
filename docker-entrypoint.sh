#!/bin/bash
# ====================================
# Whisper-Insights - Docker Entrypoint
# ====================================

set -e

# Configurar logs
echo "🐳 Iniciando Whisper-Insights no Docker..."
echo "📅 $(date)"
echo "🔧 Usuário: $(whoami)"
echo "📁 Diretório: $(pwd)"

# Verificar arquivos de configuração
if [ -f ".env" ]; then
    echo "✅ Arquivo .env encontrado"
else
    echo "⚠️ Arquivo .env não encontrado, usando .env.example como base"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env criado a partir do .env.example"
    fi
fi

# Verificar dependências críticas
echo "🔍 Verificando dependências..."

# Verificar ffmpeg
if command -v ffmpeg >/dev/null 2>&1; then
    echo "✅ ffmpeg disponível: $(ffmpeg -version | head -n1)"
else
    echo "❌ ffmpeg não encontrado!"
    exit 1
fi

# Verificar Python e dependências
echo "🐍 Python: $(python --version)"
echo "📦 Verificando pacotes Python críticos..."

python -c "import flask; print('✅ Flask:', flask.__version__)" || exit 1
python -c "import whisper; print('✅ OpenAI Whisper disponível')" || exit 1
python -c "import torch; print('✅ PyTorch:', torch.__version__)" || exit 1

# Verificar estrutura de diretórios
echo "📁 Verificando estrutura de diretórios..."
for dir in uploads logs public templates services helpers; do
    if [ -d "$dir" ]; then
        echo "✅ Diretório $dir existe"
    else
        echo "⚠️ Criando diretório $dir"
        mkdir -p "$dir"
    fi
done

# Verificar permissões
echo "🔐 Verificando permissões..."
# Tentar corrigir permissões primeiro
chown -R whisper:whisper uploads logs 2>/dev/null || true
chmod -R 755 uploads logs 2>/dev/null || true

if [ -w uploads ] && [ -w logs ]; then
    echo "✅ Permissões de escrita OK"
else
    echo "⚠️ Problemas de permissão detectados, tentando correção..."
    # Tentar criar os diretórios novamente com permissões corretas
    mkdir -p uploads logs
    chown -R whisper:whisper uploads logs 2>/dev/null || true
    chmod -R 755 uploads logs 2>/dev/null || true

    if [ -w uploads ] && [ -w logs ]; then
        echo "✅ Permissões corrigidas com sucesso"
    else
        echo "⚠️ Permissões limitadas, mas continuando execução"
    fi
fi

# Configurar logging
export PYTHONPATH=/app
export PYTHONUNBUFFERED=1

# Verificar saúde dos serviços opcionais
echo "🔍 Verificando serviços opcionais..."

# Verificar Ollama (opcional)
if [ ! -z "$OLLAMA_BASE_URL" ]; then
    echo "🤖 Verificando Ollama em $OLLAMA_BASE_URL"
    if curl -s "$OLLAMA_BASE_URL/api/tags" >/dev/null 2>&1; then
        echo "✅ Ollama disponível"
    else
        echo "⚠️ Ollama não disponível (continuando sem insights de IA)"
    fi
fi

# Verificar token Hugging Face (opcional)
if [ ! -z "$HUGGING_FACE_TOKEN" ]; then
    echo "🤗 Token Hugging Face configurado (diarização disponível)"
else
    echo "⚠️ Token Hugging Face não configurado (diarização indisponível)"
fi

# Limpar cache antigo se necessário
echo "🧹 Limpeza de cache..."
find uploads -name "*.tmp" -mtime +1 -delete 2>/dev/null || true

# Configurar timezone (se especificado)
if [ ! -z "$TZ" ]; then
    echo "🌍 Configurando timezone para $TZ"
    export TZ
fi

echo "🚀 Configuração concluída, iniciando aplicação..."
echo "🌐 Aplicação estará disponível em http://localhost:5001"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Executar comando
exec "$@"