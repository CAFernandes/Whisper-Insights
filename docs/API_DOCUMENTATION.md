# 🔌 Documentação da API - Whisper-Insights

Esta documentação detalha todos os endpoints da API REST do Whisper-Insights, permitindo integração programática com a aplicação.

## 📋 Visão Geral

O Whisper-Insights expõe uma API RESTful que permite:
- Upload e processamento de arquivos de áudio/vídeo
- Monitoramento do status de processamento
- Recuperação de resultados de transcrição
- Geração de insights com IA

**Base URL**: `http://localhost:5001/api`

## 🔐 Autenticação

Atualmente, a API não requer autenticação. Para uso em produção, considere implementar:
- API Keys
- JWT Tokens
- OAuth 2.0

## 📡 Endpoints

### 1. Upload e Processamento de Arquivo

#### `POST /upload`

Faz upload de um arquivo de áudio/vídeo e inicia o processamento.

**Parâmetros:**
- `file` (form-data, obrigatório): Arquivo de áudio/vídeo
- `enable_diarization` (form-data, opcional): `true` ou `false` (padrão: `false`)
- `generate_insights` (form-data, opcional): `true` ou `false` (padrão: `false`)
- `min_speakers` (form-data, opcional): Número mínimo de locutores (padrão: 1)
- `max_speakers` (form-data, opcional): Número máximo de locutores (padrão: 10)

**Exemplo de Requisição:**
```bash
curl -X POST http://localhost:5001/upload \
  -F "file=@audio.mp3" \
  -F "enable_diarization=true" \
  -F "generate_insights=true" \
  -F "min_speakers=1" \
  -F "max_speakers=5"
```

**Resposta de Sucesso (200):**
```json
{
  "status": "success",
  "message": "Arquivo recebido. Processamento iniciado.",
  "task_id": "task_1703123456789",
  "filename": "audio.mp3"
}
```

**Resposta de Erro (400):**
```json
{
  "status": "error",
  "message": "Nenhum arquivo foi enviado."
}
```

**Códigos de Status:**
- `200`: Upload realizado com sucesso
- `400`: Erro na requisição (arquivo inválido, formato não suportado, etc.)
- `413`: Arquivo muito grande
- `500`: Erro interno do servidor

### 2. Status da Tarefa

#### `GET /task-status/<task_id>`

Retorna o status atual de uma tarefa de processamento.

**Parâmetros:**
- `task_id` (URL, obrigatório): ID da tarefa retornado pelo endpoint de upload

**Exemplo de Requisição:**
```bash
curl http://localhost:5001/task-status/task_1703123456789
```

**Resposta - Processando (200):**
```json
{
  "status": "processing",
  "progress": "Transcrevendo áudio...",
  "task_id": "task_1703123456789"
}
```

**Resposta - Concluído (200):**
```json
{
  "status": "completed",
  "task_id": "task_1703123456789",
  "results": {
    "transcription": {
      "simple_text": "Olá, como você está hoje?",
      "timestamped_text": "[00:00 - 00:03] Olá, como você está hoje?",
      "diarized_text": "[00:00 - 00:03] SPEAKER_00: Olá, como você está hoje?"
    },
    "diarization": {
      "enabled": true,
      "speakers_summary": {
        "SPEAKER_00": {
          "duration": 15.5,
          "percentage": 60.2
        }
      }
    },
    "insights": {
      "summary": "Resumo executivo da conversa...",
      "topics": ["Saudações", "Estado pessoal"],
      "sentiment": "Neutro/Positivo"
    },
    "metadata": {
      "duration": 25.8,
      "model_used": "base",
      "processing_time": 12.3,
      "file_size": 1048576
    }
  }
}
```

**Resposta - Erro (200):**
```json
{
  "status": "error",
  "message": "Erro durante a transcrição: formato de arquivo não suportado",
  "task_id": "task_1703123456789"
}
```

**Resposta - Tarefa Não Encontrada (404):**
```json
{
  "status": "error",
  "message": "Tarefa não encontrada"
}
```

### 3. Listar Tarefas

#### `GET /tasks`

Lista todas as tarefas em andamento ou recentes.

**Parâmetros de Query (opcionais):**
- `status`: Filtrar por status (`processing`, `completed`, `error`)
- `limit`: Número máximo de resultados (padrão: 50)

**Exemplo de Requisição:**
```bash
curl "http://localhost:5001/tasks?status=completed&limit=10"
```

**Resposta (200):**
```json
{
  "status": "success",
  "tasks": [
    {
      "task_id": "task_1703123456789",
      "status": "completed",
      "filename": "audio.mp3",
      "created_at": "2024-12-21T10:30:45Z",
      "completed_at": "2024-12-21T10:32:15Z"
    }
  ],
  "total": 1
}
```

### 4. Download de Resultado

#### `GET /download/<task_id>/<format>`

Baixa o resultado da transcrição em diferentes formatos.

**Parâmetros:**
- `task_id` (URL, obrigatório): ID da tarefa
- `format` (URL, obrigatório): Formato desejado (`txt`, `json`, `srt`, `vtt`)

**Formatos Disponíveis:**
- `txt`: Texto simples
- `json`: JSON completo com todos os dados
- `srt`: Legendas SubRip
- `vtt`: Legendas WebVTT

**Exemplo de Requisição:**
```bash
curl http://localhost:5001/download/task_1703123456789/txt -o transcricao.txt
```

**Resposta (200):**
```
Content-Type: text/plain (para txt)
Content-Type: application/json (para json)
Content-Type: text/srt (para srt)
Content-Type: text/vtt (para vtt)

[Conteúdo do arquivo no formato solicitado]
```

### 5. Saúde da API

#### `GET /health`

Verifica o status de saúde da aplicação e seus componentes.

**Exemplo de Requisição:**
```bash
curl http://localhost:5001/health
```

**Resposta (200):**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-21T10:30:45Z",
  "services": {
    "whisper": {
      "status": "operational",
      "model": "base",
      "gpu_available": false
    },
    "ollama": {
      "status": "operational",
      "url": "http://localhost:11434",
      "models": ["llama3.2:3b"]
    },
    "diarization": {
      "status": "operational",
      "token_configured": true
    }
  },
  "system": {
    "cpu_usage": 25.3,
    "memory_usage": 45.8,
    "disk_free": "15.2 GB"
  }
}
```

### 6. Configurações

#### `GET /config`

Retorna as configurações públicas da aplicação.

**Exemplo de Requisição:**
```bash
curl http://localhost:5001/config
```

**Resposta (200):**
```json
{
  "status": "success",
  "config": {
    "max_file_size_mb": 500,
    "allowed_extensions": ["mp3", "wav", "m4a", "ogg", "flac", "mp4", "avi", "kwf"],
    "whisper_model": "base",
    "diarization_enabled": true,
    "insights_enabled": true,
    "supported_languages": ["pt", "en", "es", "fr", "de"]
  }
}
```

## 📝 Modelos de Dados

### Task Object
```json
{
  "task_id": "string",
  "status": "processing|completed|error",
  "progress": "string",
  "filename": "string",
  "created_at": "ISO 8601 datetime",
  "completed_at": "ISO 8601 datetime",
  "error_message": "string"
}
```

### Results Object
```json
{
  "transcription": {
    "simple_text": "string",
    "timestamped_text": "string",
    "diarized_text": "string"
  },
  "diarization": {
    "enabled": boolean,
    "speakers_summary": {
      "SPEAKER_XX": {
        "duration": number,
        "percentage": number
      }
    }
  },
  "insights": {
    "summary": "string",
    "topics": ["string"],
    "sentiment": "string",
    "actions": ["string"],
    "decisions": ["string"]
  },
  "metadata": {
    "duration": number,
    "model_used": "string",
    "processing_time": number,
    "file_size": number,
    "language": "string"
  }
}
```

## 💻 Exemplos de Integração

### Python
```python
import requests
import time

# Upload de arquivo
def transcribe_audio(file_path, enable_diarization=True, generate_insights=True):
    url = "http://localhost:5001/upload"

    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'enable_diarization': str(enable_diarization).lower(),
            'generate_insights': str(generate_insights).lower()
        }

        response = requests.post(url, files=files, data=data)
        result = response.json()

        if result['status'] == 'success':
            return result['task_id']
        else:
            raise Exception(result['message'])

# Monitorar progresso
def wait_for_completion(task_id, max_wait=300):
    url = f"http://localhost:5001/task-status/{task_id}"

    start_time = time.time()
    while time.time() - start_time < max_wait:
        response = requests.get(url)
        result = response.json()

        if result['status'] == 'completed':
            return result['results']
        elif result['status'] == 'error':
            raise Exception(result['message'])

        print(f"Status: {result.get('progress', 'Processando...')}")
        time.sleep(5)

    raise TimeoutError("Timeout aguardando conclusão")

# Uso
task_id = transcribe_audio("audio.mp3")
results = wait_for_completion(task_id)
print(results['transcription']['simple_text'])
```

### JavaScript/Node.js
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function transcribeAudio(filePath, options = {}) {
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    form.append('enable_diarization', options.diarization || 'false');
    form.append('generate_insights', options.insights || 'false');

    try {
        const response = await axios.post('http://localhost:5001/upload', form, {
            headers: form.getHeaders()
        });

        return response.data.task_id;
    } catch (error) {
        throw new Error(error.response.data.message);
    }
}

async function getTaskStatus(taskId) {
    try {
        const response = await axios.get(`http://localhost:5001/task-status/${taskId}`);
        return response.data;
    } catch (error) {
        throw new Error('Erro ao consultar status da tarefa');
    }
}

async function waitForCompletion(taskId, maxWait = 300000) {
    const startTime = Date.now();

    while (Date.now() - startTime < maxWait) {
        const status = await getTaskStatus(taskId);

        if (status.status === 'completed') {
            return status.results;
        } else if (status.status === 'error') {
            throw new Error(status.message);
        }

        console.log(`Status: ${status.progress || 'Processando...'}`);
        await new Promise(resolve => setTimeout(resolve, 5000));
    }

    throw new Error('Timeout aguardando conclusão');
}

// Uso
(async () => {
    try {
        const taskId = await transcribeAudio('audio.mp3', {
            diarization: true,
            insights: true
        });
        const results = await waitForCompletion(taskId);
        console.log(results.transcription.simple_text);
    } catch (error) {
        console.error('Erro:', error.message);
    }
})();
```

### cURL Examples
```bash
# Upload básico
curl -X POST http://localhost:5001/upload \
  -F "file=@audio.mp3"

# Upload com todas as opções
curl -X POST http://localhost:5001/upload \
  -F "file=@meeting.wav" \
  -F "enable_diarization=true" \
  -F "generate_insights=true" \
  -F "min_speakers=2" \
  -F "max_speakers=8"

# Verificar status
curl http://localhost:5001/task-status/task_1703123456789

# Download como JSON
curl http://localhost:5001/download/task_1703123456789/json -o result.json

# Download como SRT
curl http://localhost:5001/download/task_1703123456789/srt -o subtitles.srt

# Verificar saúde
curl http://localhost:5001/health
```

## 🚨 Códigos de Erro

### Códigos HTTP
- `200`: Sucesso
- `400`: Erro na requisição (parâmetros inválidos, arquivo não suportado)
- `404`: Recurso não encontrado (tarefa, endpoint)
- `413`: Arquivo muito grande
- `422`: Erro de processamento
- `500`: Erro interno do servidor
- `503`: Serviço indisponível (Ollama offline, etc.)

### Códigos de Erro Personalizados
```json
{
  "error_code": "FILE_TOO_LARGE",
  "message": "Arquivo excede o limite de 500MB",
  "details": {
    "max_size_mb": 500,
    "file_size_mb": 750
  }
}
```

## 🔧 Limitações e Considerações

### Rate Limiting
- Não implementado na versão atual
- Para produção, considere implementar rate limiting

### Timeouts
- Upload: 30 segundos
- Processamento: Configurável via `OLLAMA_REQUEST_TIMEOUT_SECONDS`
- API calls: 30 segundos por padrão

### Tamanho de Arquivo
- Máximo configurável via `MAX_FILE_SIZE_MB`
- Padrão: 500MB

### Formatos Suportados
- Áudio: mp3, wav, m4a, ogg, flac
- Vídeo: mp4, avi
- Especiais: kwf (com fallback automático)

## 📈 Monitoramento

### Logs de API
Todas as requisições são logadas em `app.log`:
```
2024-12-21 10:30:45 - INFO - API: POST /upload - Status: 200 - Time: 0.15s
2024-12-21 10:30:50 - INFO - API: GET /task-status/task_1703123456789 - Status: 200 - Time: 0.02s
```

### Métricas Disponíveis
- Número de uploads por hora
- Tempo médio de processamento
- Taxa de sucesso/erro
- Uso de recursos do sistema

---

**💡 Dica**: Use o endpoint `/health` para monitoramento automatizado e alertas em sistemas de produção.
