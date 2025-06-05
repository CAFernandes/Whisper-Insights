# ⚙️ Configuração Avançada - Whisper-Insights

Este documento detalha todas as configurações disponíveis e como personalizar o Whisper-Insights para suas necessidades específicas.

## 📄 Arquivo .env

O arquivo `.env` é onde você define todas as configurações do sistema. Copie o `.env.example` e personalize conforme necessário:

```bash
cp .env.example .env
nano .env
```

## 🔧 Configurações Detalhadas

### 🌐 Configurações do Servidor

#### FLASK_SECRET_KEY
```bash
FLASK_SECRET_KEY=sua-chave-secreta-super-segura
```
- **Descrição**: Chave secreta para sessões Flask
- **Padrão**: `whisper-insights-secret-key-2025`
- **Produção**: Use uma chave aleatória e segura
- **Exemplo**: `openssl rand -hex 32`

### 📁 Configurações de Upload

#### UPLOAD_FOLDER
```bash
UPLOAD_FOLDER=uploads
```
- **Descrição**: Pasta para arquivos temporários
- **Padrão**: `uploads`
- **Caminho**: Relativo ao diretório da aplicação
- **Permissões**: A aplicação deve ter read/write

#### ALLOWED_EXTENSIONS
```bash
ALLOWED_EXTENSIONS=mp3,wav,m4a,ogg,flac,mp4,avi,kwf
```
- **Descrição**: Formatos de arquivo permitidos
- **Padrão**: Áudio e vídeo comuns
- **Customização**: Adicione/remova extensões conforme necessário
- **Exemplo**: `mp3,wav,m4a` (apenas áudio comum)

#### MAX_FILE_SIZE_MB
```bash
MAX_FILE_SIZE_MB=500
```
- **Descrição**: Tamanho máximo de arquivo em MB
- **Padrão**: 500MB
- **Recomendação**: Ajuste conforme sua infraestrutura
- **Considerações**: Arquivos maiores = mais memória/tempo

#### UPLOAD_FILE_MAX_AGE_MINUTES
```bash
UPLOAD_FILE_MAX_AGE_MINUTES=10
```
- **Descrição**: Tempo em minutos antes da limpeza automática
- **Padrão**: 10 minutos
- **Uso**: Evita acúmulo de arquivos temporários
- **Produção**: Considere valores menores (5-15 min)

### 🎙️ Configurações do Whisper

#### WHISPER_MODEL_NAME
```bash
WHISPER_MODEL_NAME=base
```

**Modelos Disponíveis:**
| Modelo | Tamanho | Velocidade | Precisão | RAM Necessária |
|---------|---------|------------|----------|----------------|
| `tiny` | 39 MB | ⚡⚡⚡⚡ | ⭐⭐ | 1GB |
| `base` | 74 MB | ⚡⚡⚡ | ⭐⭐⭐ | 1GB |
| `small` | 244 MB | ⚡⚡ | ⭐⭐⭐⭐ | 2GB |
| `medium` | 769 MB | ⚡ | ⭐⭐⭐⭐⭐ | 5GB |
| `large` | 1550 MB | 🐌 | ⭐⭐⭐⭐⭐ | 10GB |

**Recomendações:**
- **Desenvolvimento**: `tiny` ou `base`
- **Produção**: `base` ou `small`
- **Máxima Qualidade**: `medium` ou `large`
- **Recursos Limitados**: `tiny`

### 🤖 Configurações do Ollama

#### OLLAMA_API_URL
```bash
OLLAMA_API_URL=http://localhost:11434
```
- **Descrição**: URL do servidor Ollama
- **Local**: `http://localhost:11434`
- **Remoto**: `http://seu-servidor:11434`
- **Docker**: `http://ollama-container:11434`

#### OLLAMA_REQUEST_TIMEOUT_SECONDS
```bash
OLLAMA_REQUEST_TIMEOUT_SECONDS=300
```
- **Descrição**: Timeout para requisições ao Ollama
- **Padrão**: 300 segundos (5 minutos)
- **Ajuste**: Dependendo do tamanho dos arquivos
- **Produção**: Considere timeouts maiores

#### DEFAULT_INSIGHTS_PROMPT
```bash
DEFAULT_INSIGHTS_PROMPT=Analise a seguinte transcrição e forneça um resumo dos principais pontos...
```
- **Descrição**: Prompt padrão para geração de insights
- **Customização**: Adapte para seu caso de uso
- **Variável**: `{{text}}` será substituída pela transcrição
- **Idioma**: Pode ser em português, inglês, etc.

**Exemplos de Prompts Customizados:**

```bash
# Para reuniões corporativas
DEFAULT_INSIGHTS_PROMPT=Analise esta transcrição de reunião e identifique: 1) Decisões tomadas, 2) Ações definidas, 3) Responsáveis, 4) Prazos mencionados. Transcrição: {{text}}

# Para entrevistas
DEFAULT_INSIGHTS_PROMPT=Resuma esta entrevista destacando: pontos-chave do entrevistado, temas principais, insights importantes. Transcrição: {{text}}

# Para aulas/palestras
DEFAULT_INSIGHTS_PROMPT=Crie um resumo desta aula incluindo: conceitos principais, exemplos dados, pontos importantes para revisão. Conteúdo: {{text}}
```

### 🎭 Configurações de Diarização

#### ENABLE_SPEAKER_DIARIZATION
```bash
ENABLE_SPEAKER_DIARIZATION=true
```
- **Descrição**: Habilita identificação de locutores
- **Valores**: `true` ou `false`
- **Dependência**: Requer token do Hugging Face
- **Performance**: Aumenta tempo de processamento

#### DEFAULT_MIN_SPEAKERS / DEFAULT_MAX_SPEAKERS
```bash
DEFAULT_MIN_SPEAKERS=1
DEFAULT_MAX_SPEAKERS=10
```
- **Descrição**: Faixa esperada de número de locutores
- **Min**: Mínimo de pessoas esperadas
- **Max**: Máximo de pessoas esperadas
- **Otimização**: Valores precisos melhoram a performance

#### HUGGINGFACE_HUB_TOKEN
```bash
HUGGINGFACE_HUB_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- **Obrigatório**: Para usar diarização
- **Obtenção**: https://huggingface.co/settings/tokens
- **Termos**: Aceite em https://huggingface.co/pyannote/speaker-diarization-3.1
- **Tipo**: Read token é suficiente

## 🔧 Configurações por Ambiente

### Desenvolvimento
```bash
# .env.development
FLASK_SECRET_KEY=dev-key-not-secure
WHISPER_MODEL_NAME=tiny
MAX_FILE_SIZE_MB=100
OLLAMA_REQUEST_TIMEOUT_SECONDS=60
ENABLE_SPEAKER_DIARIZATION=false
```

### Produção
```bash
# .env.production
FLASK_SECRET_KEY=super-secure-random-key-here
WHISPER_MODEL_NAME=base
MAX_FILE_SIZE_MB=500
OLLAMA_REQUEST_TIMEOUT_SECONDS=300
ENABLE_SPEAKER_DIARIZATION=true
HUGGINGFACE_HUB_TOKEN=your-real-token
```

### Servidor Corporativo
```bash
# .env.corporate
UPLOAD_FOLDER=/var/whisper-insights/uploads
MAX_FILE_SIZE_MB=1000
WHISPER_MODEL_NAME=medium
OLLAMA_API_URL=http://ai-server.company.com:11434
ENABLE_SPEAKER_DIARIZATION=true
UPLOAD_FILE_MAX_AGE_MINUTES=5
```

## 🚀 Configurações de Performance

### Para Máxima Velocidade
```bash
WHISPER_MODEL_NAME=tiny
ENABLE_SPEAKER_DIARIZATION=false
MAX_FILE_SIZE_MB=50
```

### Para Máxima Qualidade
```bash
WHISPER_MODEL_NAME=large
ENABLE_SPEAKER_DIARIZATION=true
OLLAMA_REQUEST_TIMEOUT_SECONDS=600
```

### Para Ambiente com Recursos Limitados
```bash
WHISPER_MODEL_NAME=tiny
ENABLE_SPEAKER_DIARIZATION=false
MAX_FILE_SIZE_MB=100
UPLOAD_FILE_MAX_AGE_MINUTES=5
```

## 🔐 Configurações de Segurança

### Produção Segura
```bash
# Gerar chave segura
FLASK_SECRET_KEY=$(openssl rand -hex 32)

# Limitar tamanho de arquivo
MAX_FILE_SIZE_MB=200

# Limpeza frequente
UPLOAD_FILE_MAX_AGE_MINUTES=5

# Extensões restritas
ALLOWED_EXTENSIONS=mp3,wav,m4a
```

### Configurações de Rede
```bash
# Para acesso apenas local
FLASK_HOST=127.0.0.1

# Para acesso na rede
FLASK_HOST=0.0.0.0

# Porta customizada
FLASK_PORT=5001
```

## 📊 Monitoramento e Logs

### Configurações de Log
```python
# No config.py ou .env
LOG_LEVEL=INFO
LOG_FILE=app.log
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5
```

### Métricas de Performance
```bash
# Habilitar métricas detalhadas
ENABLE_PERFORMANCE_METRICS=true
METRICS_ENDPOINT=/metrics
```

## 🔄 Configurações Avançadas

### Cache e Performance
```bash
# Cache de modelos
MODEL_CACHE_DIR=/var/cache/whisper-insights

# Número de workers
WORKER_PROCESSES=4

# Timeout de processamento
PROCESSING_TIMEOUT=1800
```

### Integração com Serviços Externos
```bash
# Webhook para notificações
WEBHOOK_URL=https://hooks.slack.com/services/...

# API externa para armazenamento
STORAGE_API_URL=https://api.company.com/storage
STORAGE_API_KEY=your-api-key
```

## 🧪 Configurações para Testes

### Ambiente de Teste
```bash
# .env.test
UPLOAD_FOLDER=test_uploads
WHISPER_MODEL_NAME=tiny
ENABLE_SPEAKER_DIARIZATION=false
MAX_FILE_SIZE_MB=10
OLLAMA_REQUEST_TIMEOUT_SECONDS=30
```

### Configuração CI/CD
```bash
# Para pipelines de integração contínua
CI_MODE=true
SKIP_MODEL_DOWNLOAD=false
TEST_TIMEOUT=300
```

## 📝 Validação de Configurações

### Script de Validação
```python
# validate_config.py
import os
from config import *

def validate_config():
    """Valida todas as configurações"""
    errors = []

    # Verificar pasta de upload
    if not os.path.exists(UPLOAD_FOLDER):
        try:
            os.makedirs(UPLOAD_FOLDER)
        except Exception as e:
            errors.append(f"Não foi possível criar {UPLOAD_FOLDER}: {e}")

    # Verificar token do Hugging Face
    if ENABLE_SPEAKER_DIARIZATION and not HUGGINGFACE_HUB_TOKEN:
        errors.append("Token do Hugging Face necessário para diarização")

    # Verificar Ollama
    try:
        import requests
        response = requests.get(f"{OLLAMA_BASE_URL}/api/version", timeout=5)
        if response.status_code != 200:
            errors.append(f"Ollama não acessível em {OLLAMA_BASE_URL}")
    except:
        errors.append("Ollama não está rodando")

    return errors

if __name__ == "__main__":
    errors = validate_config()
    if errors:
        print("❌ Erros de configuração encontrados:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Todas as configurações estão válidas!")
```

## 📋 Checklist de Configuração

### Configuração Mínima
- [ ] Arquivo `.env` criado
- [ ] `FLASK_SECRET_KEY` definida
- [ ] `WHISPER_MODEL_NAME` configurado
- [ ] Pasta `uploads` existe e tem permissões

### Configuração Completa
- [ ] Token do Hugging Face configurado
- [ ] Ollama instalado e rodando
- [ ] Modelo Llama baixado no Ollama
- [ ] Testes passando
- [ ] Logs funcionando

### Configuração de Produção
- [ ] Chave secreta segura
- [ ] HTTPS configurado
- [ ] Backup automatizado
- [ ] Monitoramento ativo
- [ ] Limites de segurança definidos

---

**💡 Dica**: Use ambientes diferentes (development, staging, production) com arquivos `.env` específicos para cada um.
