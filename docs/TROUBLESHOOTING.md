# 🔧 Solução de Problemas - Whisper-Insights

Este documento fornece soluções para problemas comuns encontrados ao usar o Whisper-Insights.

## 🚨 Problemas Comuns

### 1. Erro de Instalação

#### "No module named 'whisper'"
```bash
# Problema: Módulo Whisper não encontrado
# Solução:
source transcribe/bin/activate
pip install openai-whisper
```

#### "No module named 'pyannote'"
```bash
# Problema: Diarização não funciona
# Solução:
pip install pyannote.audio
```

#### "FFmpeg not found"
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg-free

# macOS
brew install ffmpeg

# Verificar instalação
ffmpeg -version
```

### 2. Problemas de Configuração

#### Token do Hugging Face Inválido
```bash
# Sintomas: Diarização falha com erro de autenticação
# Verificação:
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://huggingface.co/api/whoami

# Soluções:
# 1. Gerar novo token em: https://huggingface.co/settings/tokens
# 2. Aceitar termos em: https://huggingface.co/pyannote/speaker-diarization-3.1
# 3. Configurar no .env:
HUGGINGFACE_HUB_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Ollama Não Responde
```bash
# Verificar se Ollama está rodando
curl http://localhost:11434/api/version

# Se não estiver rodando:
ollama serve

# Verificar modelos disponíveis
ollama list

# Baixar modelo se necessário
ollama pull llama3.2:3b
```

#### Erro de Permissões na Pasta uploads/
```bash
# Verificar permissões
ls -la uploads/

# Ajustar permissões
chmod 755 uploads/
chown -R $USER:$USER uploads/

# Se não existir, criar
mkdir -p uploads
```

### 3. Problemas de Processamento

#### "Out of Memory" Durante Transcrição
```bash
# Problema: Não há memória suficiente
# Soluções:

# 1. Usar modelo menor no .env
WHISPER_MODEL_NAME=tiny

# 2. Processar arquivos menores
MAX_FILE_SIZE_MB=100

# 3. Verificar uso de memória
free -h
top
```

#### Arquivo KWF Não Processa
```bash
# Problema: Formato KWF específico
# O sistema tem fallback automático, mas se falhar:

# 1. Converter manualmente
ffmpeg -i arquivo.kwf -c:a pcm_s16le arquivo.wav

# 2. Verificar logs
tail -f app.log

# 3. Usar formato alternativo
# Converta para MP3 ou WAV antes do upload
```

#### Timeout Durante Processamento
```bash
# Problema: Arquivo muito grande ou processamento lento
# Solução no .env:
OLLAMA_REQUEST_TIMEOUT_SECONDS=600

# Para arquivos muito grandes
OLLAMA_REQUEST_TIMEOUT_SECONDS=1800
```

### 4. Problemas de Interface Web

#### Página Não Carrega
```bash
# Verificar se aplicação está rodando
curl http://localhost:5001

# Verificar logs
tail -f app.log

# Restart da aplicação
pkill -f "python app.py"
python app.py
```

#### Upload Falha
```bash
# Verificar tamanho do arquivo
ls -lh seu_arquivo.mp3

# Se muito grande, ajustar no .env
MAX_FILE_SIZE_MB=1000

# Verificar formato suportado
file seu_arquivo.mp3
```

#### JavaScript Não Funciona
```bash
# Verificar arquivos estáticos
ls -la public/assets/js/
ls -la public/assets/css/

# Verificar permissões
chmod 644 public/assets/js/*
chmod 644 public/assets/css/*
```

### 5. Problemas de Performance

#### Processamento Muito Lento
```bash
# Soluções por prioridade:

# 1. Usar modelo menor
WHISPER_MODEL_NAME=tiny

# 2. Desabilitar diarização temporariamente
ENABLE_SPEAKER_DIARIZATION=false

# 3. Verificar CPU/GPU
nvidia-smi  # Se tiver GPU NVIDIA
htop        # Uso de CPU

# 4. Usar GPU se disponível
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### Muitos Arquivos Temporários
```bash
# Verificar limpeza automática
python cleanup_uploads.py

# Ajustar tempo de limpeza no .env
UPLOAD_FILE_MAX_AGE_MINUTES=5

# Limpeza manual
find uploads/ -type f -mmin +60 -delete
```

### 6. Problemas com Docker

#### Health Check Falhando (Erro 500)
```bash
# Sintomas: Container mostra "unhealthy" ou health check retorna HTTP 500
# Causa comum: Arquivo ollama_service.py vazio dentro do container

# Verificação do problema:
docker exec whisper-insights-app cat services/ollama_service.py
# Se o arquivo estiver vazio (0 bytes), aplicar solução:

# Solução:
docker-compose down
docker-compose build --no-cache  # Reconstrói imagem
docker-compose up -d

# Validação:
curl http://localhost:5001/health  # Deve retornar status "healthy"
docker ps  # Container deve mostrar "(healthy)"
```

#### Container Não Inicia
```bash
# Verificar logs do container
docker-compose logs whisper-insights

# Problemas comuns:
# 1. Porta em uso
lsof -i :5001
sudo kill -9 $(lsof -t -i:5001)

# 2. Permissões de volume
sudo chown -R $USER:$USER uploads logs
chmod -R 755 uploads logs

# 3. Arquivo .env ausente
cp .env.example .env

# 4. Memória insuficiente
docker system prune -f  # Liberar espaço
```

#### Ollama Não Responde
```bash
# Verificar status do container Ollama
docker ps | grep ollama

# Verificar logs
docker-compose logs ollama

# Restart apenas do Ollama
docker-compose restart ollama

# Testar conectividade
curl http://localhost:11434/api/tags
```

## 🔍 Diagnóstico Avançado

### Script de Diagnóstico Automático
```bash
# Criar script de diagnóstico
cat > diagnose.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
from config import *

def check_python():
    print(f"✓ Python: {sys.version}")
    return True

def check_dependencies():
    try:
        import whisper
        print(f"✓ Whisper: {whisper.__version__}")
    except ImportError:
        print("✗ Whisper não instalado")
        return False

    try:
        import torch
        print(f"✓ PyTorch: {torch.__version__}")
        print(f"✓ CUDA disponível: {torch.cuda.is_available()}")
    except ImportError:
        print("✗ PyTorch não instalado")
        return False

    return True

def check_config():
    print(f"✓ Pasta uploads: {os.path.exists(UPLOAD_FOLDER)}")
    print(f"✓ Token HF configurado: {bool(HUGGINGFACE_TOKEN)}")
    print(f"✓ Diarização habilitada: {ENABLE_SPEAKER_DIARIZATION}")
    return True

def check_ollama():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/version", timeout=5)
        if response.status_code == 200:
            print(f"✓ Ollama: {response.json().get('version', 'OK')}")
            return True
    except:
        pass
    print("✗ Ollama não acessível")
    return False

def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg: {version}")
            return True
    except FileNotFoundError:
        pass
    print("✗ FFmpeg não encontrado")
    return False

if __name__ == "__main__":
    print("🔍 Diagnóstico do Whisper-Insights\n")

    checks = [
        check_python,
        check_dependencies,
        check_config,
        check_ollama,
        check_ffmpeg
    ]

    results = [check() for check in checks]

    print("\n" + "="*50)
    if all(results):
        print("✅ Todos os componentes estão funcionando!")
    else:
        print("❌ Alguns problemas foram encontrados.")
        print("Consulte a documentação para soluções.")
EOF

python diagnose.py
```

### Verificação de Logs
```bash
# Logs da aplicação
tail -f app.log

# Logs do sistema
journalctl -f -u whisper-insights  # Se usando systemd

# Logs específicos por tipo
grep "ERROR" app.log
grep "WARNING" app.log
grep "CRITICAL" app.log
```

### Teste de Componentes Individuais
```bash
# Testar Whisper isoladamente
python -c "
import whisper
model = whisper.load_model('tiny')
print('✅ Whisper OK')
"

# Testar diarização
python -c "
from services.diarization_service import load_diarization_model
load_diarization_model()
print('✅ Diarização OK')
"

# Testar Ollama
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2:3b", "prompt": "Hello", "stream": false}'
```

## 📊 Monitoramento e Métricas

### Monitoramento de Recursos
```bash
# CPU e Memória
htop

# Espaço em disco
df -h

# Processos Python
ps aux | grep python

# Conexões de rede
netstat -tulpn | grep :5001
```

### Métricas da Aplicação
```bash
# Número de uploads hoje
grep "$(date +%Y-%m-%d)" app.log | grep "POST /upload" | wc -l

# Tempo médio de processamento
grep "Processing completed" app.log | tail -10

# Erros recentes
grep "ERROR" app.log | tail -5
```

## 🚨 Problemas Críticos

### Aplicação Não Inicia
```bash
# Verificações em ordem:

# 1. Ambiente virtual ativo?
which python
# Deve mostrar: /path/to/whisper-insights/transcribe/bin/python

# 2. Dependências instaladas?
pip list | grep -E "(whisper|flask|torch)"

# 3. Porta em uso?
lsof -i :5001
# Se em uso, matar processo:
sudo kill -9 $(lsof -t -i:5001)

# 4. Arquivo de configuração?
ls -la .env

# 5. Permissões corretas?
ls -la app.py
# Deve ser legível e executável
```

### Erro "Address already in use"
```bash
# Encontrar processo usando a porta
lsof -i :5001

# Matar processo
sudo kill -9 PID_DO_PROCESSO

# Ou usar porta diferente no .env
FLASK_PORT=5002
```

### Erro de Importação de Módulos
```bash
# Verificar PYTHONPATH
echo $PYTHONPATH

# Verificar ambiente virtual
which python
pip list

# Reinstalar dependências
pip install --force-reinstall -r requirements-web.txt
```

### Banco de Dados de Tarefas Corrompido
```bash
# Reset completo do sistema de tarefas
# (dados em memória serão perdidos)
pkill -f "python app.py"
rm -f task_storage.json  # Se existir
python app.py
```

## 🔄 Recuperação de Sistema

### Reset Completo
```bash
# Backup de configurações importantes
cp .env .env.backup
cp -r uploads/ uploads_backup/

# Limpar tudo
rm -rf __pycache__/
rm -rf */__pycache__/
rm -f app.log
rm -rf uploads/*

# Reinstalar dependências
source transcribe/bin/activate
pip install --force-reinstall -r requirements-web.txt

# Restaurar configurações
cp .env.backup .env

# Testar
python app.py
```

### Recuperação de Arquivos
```bash
# Se uploads foram perdidos
mkdir -p uploads
chmod 755 uploads

# Se configuração foi perdida
cp .env.example .env
# Editar manualmente as configurações
```

## 📞 Quando Buscar Ajuda

### Informações para Coleta
Ao reportar problemas, inclua:

1. **Versão do Sistema**:
   ```bash
   uname -a
   python --version
   pip list | grep -E "(whisper|torch|flask)"
   ```

2. **Logs Relevantes**:
   ```bash
   tail -50 app.log
   ```

3. **Configuração**:
   ```bash
   cat .env | grep -v TOKEN  # Omitir tokens sensíveis
   ```

4. **Erro Específico**:
   - Mensagem de erro completa
   - Passos para reproduzir
   - Arquivos que causam problema

### Recursos de Suporte
- **Documentação**: Pasta `docs/`
- **Testes Automáticos**: `python -m pytest tests/ -v`
- **Logs Detalhados**: `app.log`
- **Scripts de Diagnóstico**: `diagnose.py`

## 🔧 Ferramentas de Debug

### Modo Debug da Aplicação
```bash
# No .env
FLASK_DEBUG=true

# Ou via variável de ambiente
FLASK_DEBUG=1 python app.py
```

### Logging Detalhado
```python
# No config.py, adicionar:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Teste de Componentes
```bash
# Executar testes específicos
python -m pytest tests/test_units.py::test_whisper_service -v
python -m pytest tests/test_complete_workflow.py -v
```

---

**💡 Dica**: Mantenha sempre backups de suas configurações (arquivo `.env`) e monitore regularmente os logs em `app.log` para identificar problemas antes que se tornem críticos.
