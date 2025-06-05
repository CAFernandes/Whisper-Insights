# 📦 Guia de Instalação - Whisper-Insights

Este guia fornece instruções detalhadas para instalar e configurar o Whisper-Insights em diferentes ambientes.

## 🎯 Requisitos do Sistema

### Requisitos Mínimos
- **Python**: 3.8 ou superior
- **RAM**: 4GB (8GB recomendado para modelos maiores)
- **Espaço em Disco**: 2GB livres
- **Sistema Operacional**: Linux, macOS, Windows

### Requisitos Recomendados
- **Python**: 3.10+
- **RAM**: 8GB ou mais
- **GPU**: NVIDIA com CUDA (opcional, para melhor performance)
- **Espaço em Disco**: 5GB livres

## 🚀 Instalação Rápida

### 1. Download do Projeto
```bash
# Via Git (recomendado)
git clone <repository-url> whisper-insights
cd whisper-insights

# Ou baixe e extraia o arquivo ZIP
```

### 2. Configuração do Ambiente Python
```bash
# Criar ambiente virtual
python3 -m venv transcribe

# Ativar ambiente virtual
# Linux/macOS:
source transcribe/bin/activate

# Windows:
transcribe\Scripts\activate
```

### 3. Instalação de Dependências
```bash
# Instalar dependências principais
pip install -r requirements-web.txt

# Para funcionalidades avançadas (diarização)
pip install pyannote.audio
```

### 4. Configuração Inicial
```bash
# Copiar arquivo de configuração
cp .env.example .env

# Editar configurações
nano .env  # ou seu editor preferido
```

### 5. Primeiro Teste
```bash
# Iniciar aplicação
python app.py

# Acesse: http://localhost:5001
```

## ⚙️ Configuração Avançada

### Configuração do Ollama (Para Insights com IA)
```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Baixar modelo Llama
ollama pull llama3.2:3b

# Verificar se está funcionando
curl http://localhost:11434/api/version
```

### Configuração de Diarização (Identificação de Locutores)
1. **Criar conta no Hugging Face**: https://huggingface.co/join
2. **Gerar token**: https://huggingface.co/settings/tokens
3. **Aceitar termos**: https://huggingface.co/pyannote/speaker-diarization-3.1
4. **Configurar no .env**:
   ```bash
   HUGGINGFACE_HUB_TOKEN=seu_token_aqui
   ```

### Configuração de GPU (Opcional)
```bash
# Para NVIDIA GPU com CUDA
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verificar CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

## 🐧 Instalação no Linux

### Ubuntu/Debian
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências do sistema
sudo apt install -y python3 python3-pip python3-venv ffmpeg

# Continuar com instalação padrão...
```

### CentOS/RHEL/Fedora
```bash
# CentOS/RHEL
sudo yum install -y python3 python3-pip ffmpeg-free

# Fedora
sudo dnf install -y python3 python3-pip ffmpeg

# Continuar com instalação padrão...
```

## 🍎 Instalação no macOS

### Com Homebrew
```bash
# Instalar Homebrew (se necessário)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependências
brew install python3 ffmpeg

# Continuar com instalação padrão...
```

## 🪟 Instalação no Windows

### Pré-requisitos
1. **Python 3.8+**: https://python.org/downloads/
2. **Git** (opcional): https://git-scm.com/download/win
3. **FFmpeg** (opcional): https://ffmpeg.org/download.html

### Instalação
```cmd
# No Command Prompt ou PowerShell
python -m venv transcribe
transcribe\Scripts\activate
pip install -r requirements-web.txt
```

## 🔧 Instalação para Desenvolvimento

### Setup Completo
```bash
# Clonar repositório
git clone <repository-url> whisper-insights
cd whisper-insights

# Ambiente virtual
python3 -m venv transcribe
source transcribe/bin/activate

# Dependências completas
pip install -r requirements-web.txt
pip install pyannote.audio pytest

# Configuração
cp .env.example .env

# Testes
python -m pytest tests/ -v
```

### Dependências Adicionais para Desenvolvimento
```bash
# Ferramentas de desenvolvimento
pip install black flake8 mypy
pip install jupyter notebook

# Para debugging
pip install ipdb
```

## 📋 Verificação da Instalação

### Script de Verificação
```bash
# Executar testes básicos
python -c "
import torch
import whisper
import flask
print('✅ Todas as dependências principais estão instaladas!')
print(f'🐍 Python: {__import__('sys').version}')
print(f'🔥 PyTorch: {torch.__version__}')
print(f'🎙️ Whisper: {whisper.__version__}')
print(f'🌐 Flask: {flask.__version__}')
"

# Testar aplicação
python app.py &
sleep 5
curl -f http://localhost:5001 && echo "✅ Aplicação funcionando!"
```

### Checklist de Verificação
- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual ativo
- [ ] Dependências instaladas sem erros
- [ ] Arquivo .env configurado
- [ ] Aplicação inicia sem erros
- [ ] Interface web acessível
- [ ] Upload de arquivo funciona
- [ ] Transcrição básica funciona

## 🐛 Problemas Comuns

### Erro: "No module named 'whisper'"
```bash
# Reativar ambiente virtual
source transcribe/bin/activate
pip install openai-whisper
```

### Erro: "FFmpeg not found"
```bash
# Linux
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows: baixar de https://ffmpeg.org/
```

### Erro de Memória
```bash
# Usar modelo menor no .env
WHISPER_MODEL_NAME=tiny
```

### Problemas de Permissão
```bash
# Linux/macOS
chmod +x start_web.sh

# Se necessário
sudo chown -R $USER:$USER whisper-insights/
```

## 🚀 Deploy em Produção

### Com Gunicorn
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Com Docker (em desenvolvimento)
```dockerfile
# Dockerfile básico
FROM python:3.10-slim
WORKDIR /app
COPY requirements-web.txt .
RUN pip install -r requirements-web.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
```

## 📞 Suporte

### Logs e Debugging
```bash
# Verificar logs
tail -f app.log

# Modo debug
export FLASK_DEBUG=1
python app.py
```

### Recursos de Ajuda
- **Documentação**: Pasta `docs/`
- **Testes**: `python -m pytest tests/ -v`
- **Logs**: Arquivo `app.log`
- **Configuração**: Arquivo `.env`

### Problemas Conhecidos
- Consulte `docs/TROUBLESHOOTING.md`
- Verifique `app.log` para detalhes de erros
- Execute testes para validar instalação

---

**💡 Dica**: Para instalação em ambiente corporativo, considere usar `pip install --user` ou configurar um registry interno do PyPI.
