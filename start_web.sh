#!/bin/bash

# Script para iniciar o Transcritor de Áudio Web

echo "🎙️ Transcritor de Áudio Web"
echo "=========================="

# Verificar se estamos no diretório correto
if [ ! -f "app.py" ]; then
    echo "❌ Erro: Execute este script no diretório do projeto (onde está o app.py)"
    exit 1
fi

# Ativar ambiente virtual
if [ -d "transcribe" ]; then
    echo "📦 Ativando ambiente virtual..."
    source transcribe/bin/activate
else
    echo "❌ Erro: Ambiente virtual 'transcribe' não encontrado"
    echo "   Execute primeiro: python3 -m venv transcribe && source transcribe/bin/activate"
    exit 1
fi

# Verificar se as dependências estão instaladas
echo "🔍 Verificando dependências..."
python -c "import flask, whisper" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Instalando dependências..."
    pip install -r requirements-web.txt
fi

# Verificar ffmpeg
echo "🔧 Verificando ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  AVISO: ffmpeg não encontrado"
    echo "   Para instalar: sudo apt install ffmpeg"
    echo "   Alguns formatos de áudio podem não funcionar sem ffmpeg"
    echo ""
fi

# Iniciar aplicação
echo "🚀 Iniciando servidor web..."
echo "📡 Acesse: http://localhost:5000"
echo "🛑 Para parar: Ctrl+C"
echo ""

python app.py
