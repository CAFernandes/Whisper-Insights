#!/bin/bash

# 🎬 Demonstração da Aplicação Web de Transcrição de Áudio

echo "🎙️ DEMONSTRAÇÃO - Transcritor de Áudio Web"
echo "=========================================="
echo ""

echo "📍 Você está em: $(pwd)"
echo ""

echo "📁 Arquivos criados para a versão web:"
echo "   ✅ app.py                 - Servidor Flask"
echo "   ✅ templates/index.html   - Interface moderna"
echo "   ✅ start_web.sh          - Script de inicialização"
echo "   ✅ requirements-web.txt   - Dependências"
echo "   ✅ README-WEB.md         - Documentação"
echo ""

echo "🔍 Verificando arquivos..."
if [ -f "app.py" ]; then
    echo "   ✅ app.py encontrado"
else
    echo "   ❌ app.py não encontrado"
fi

if [ -f "templates/index.html" ]; then
    echo "   ✅ templates/index.html encontrado"
else
    echo "   ❌ templates/index.html não encontrado"
fi

if [ -d "transcribe" ]; then
    echo "   ✅ Ambiente virtual encontrado"
else
    echo "   ❌ Ambiente virtual não encontrado"
fi

echo ""

echo "🚀 Para iniciar a aplicação web:"
echo ""
echo "   Método 1 (Recomendado):"
echo "   ./start_web.sh"
echo ""
echo "   Método 2 (Manual):"
echo "   source transcribe/bin/activate"
echo "   python app.py"
echo ""

echo "🌐 Depois de iniciar, acesse:"
echo "   http://localhost:5000"
echo ""

echo "🎯 Funcionalidades disponíveis:"
echo "   📤 Upload via drag & drop ou botão"
echo "   🎙️ Transcrição com IA Whisper"
echo "   📋 Copiar texto transcrito"
echo "   💾 Download do resultado"
echo "   📱 Interface responsiva"
echo "   🔄 Processamento assíncrono"
echo ""

echo "📋 Formatos suportados:"
echo "   🎵 Áudio: mp3, wav, m4a, ogg, flac"
echo "   🎬 Vídeo: mp4, avi"
echo ""

echo "💡 Dicas de uso:"
echo "   • Arraste o arquivo diretamente para a página"
echo "   • Aguarde o carregamento do modelo na primeira vez"
echo "   • Use Ctrl+C para parar o servidor"
echo "   • Arquivos são removidos automaticamente após processamento"
echo ""

echo "🎉 Sua aplicação está pronta para uso!"
echo "🔥 Interface moderna, responsiva e profissional!"
