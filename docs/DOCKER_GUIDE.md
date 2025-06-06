# 🐳 Guia Docker - Whisper-Insights

Este documento fornece informações detalhadas sobre o uso do Whisper-Insights com Docker.

## 🚀 Início Rápido

### Pré-requisitos
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM disponível
- 10GB espaço em disco

### Comandos Básicos
```bash
# Iniciar aplicação
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f

# Parar aplicação
docker-compose down
```

## 📋 Makefile - Comandos Disponíveis

O projeto inclui um Makefile com comandos úteis:

```bash
# Ver todos os comandos disponíveis
make help

# Comandos principais
make build      # Constrói as imagens
make up         # Inicia serviços
make down       # Para serviços
make logs       # Mostra logs
make health     # Verifica saúde dos serviços
make restart    # Reinicia serviços
```

## 🏥 Health Check e Monitoramento

### Verificação de Saúde
```bash
# Health check da aplicação
curl http://localhost:5001/health

# Verificar status do Docker
docker ps

# Logs específicos
docker-compose logs whisper-insights
docker-compose logs ollama
```

### Resposta do Health Check
```json
{
  "status": "healthy",
  "timestamp": 1749212241.076,
  "services": {
    "whisper": {
      "status": "available",
      "model": "base"
    },
    "uploads": {
      "status": "accessible",
      "path": "uploads"
    },
    "ollama": {
      "status": "unavailable",
      "url": "http://localhost:11434"
    },
    "diarization": {
      "status": "available"
    }
  },
  "version": "1.0.0",
  "uptime": 1749212241.076
}
```

## 🔧 Configuração

### Arquivo .env
```bash
# Copiar configuração exemplo
cp .env.example .env

# Editar configurações
nano .env
```

### Principais Configurações
```env
# Aplicação
FLASK_SECRET_KEY=your-secret-key
FLASK_RUN_PORT=5001

# Whisper
WHISPER_MODEL_NAME=base  # tiny, base, small, medium, large

# Upload
MAX_FILE_SIZE_MB=500
UPLOAD_FILE_MAX_AGE_MINUTES=30

# Ollama (opcional)
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_DEFAULT_MODEL=llama3.2

# Diarização (opcional)
HUGGING_FACE_TOKEN=hf_your_token_here
DIARIZATION_ENABLED=true
```

## 📁 Volumes e Persistência

### Volumes Automáticos
- `uploads/` - Arquivos enviados pelos usuários
- `logs/` - Logs da aplicação
- `whisper_models/` - Cache dos modelos Whisper
- `huggingface_cache/` - Cache do Hugging Face
- `ollama_data/` - Dados e modelos do Ollama

### Backup de Volumes
```bash
# Listar volumes
docker volume ls | grep whisper

# Backup completo
make backup-volumes

# Backup manual
docker run --rm -v whispper_insights_whisper_models:/data \
  -v $(pwd):/backup alpine tar czf /backup/whisper_models.tar.gz /data
```

## 🌐 Modo Produção

### Com Nginx (Recomendado)
```bash
# Iniciar com proxy reverso
docker-compose --profile production up -d

# Acesso via HTTP
curl http://localhost/health
```

### Configurações de Produção
- SSL/TLS configurado no Nginx
- Rate limiting habilitado
- Logs estruturados
- Health checks automáticos

## 🛠️ Desenvolvimento

### Modo Desenvolvimento
```bash
# Iniciar com logs visíveis
docker-compose up

# Rebuild completo
docker-compose up --build

# Acessar container
docker exec -it whisper-insights-app bash
```

### Debug de Problemas
```bash
# Verificar recursos
docker stats

# Inspecionar container
docker inspect whisper-insights-app

# Logs detalhados
docker-compose logs --tail=100 whisper-insights
```

## 🚨 Solução de Problemas

### Health Check Falhando
```bash
# Verificar se arquivo ollama_service.py está correto
docker exec whisper-insights-app ls -la services/ollama_service.py

# Se arquivo estiver vazio (0 bytes):
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Validar correção
curl http://localhost:5001/health
```

### Container Não Inicia
```bash
# Verificar logs de erro
docker-compose logs whisper-insights

# Problemas comuns:
# 1. Porta ocupada
sudo lsof -i :5001

# 2. Memória insuficiente
docker system prune -f

# 3. Permissões
sudo chown -R $USER:$USER uploads logs
```

### Ollama Problemas
```bash
# Status do Ollama
curl http://localhost:11434/api/tags

# Reiniciar apenas Ollama
docker-compose restart ollama

# Baixar modelos
docker exec whisper-insights-ollama ollama pull llama3.2
```

## 📊 Monitoramento

### Métricas do Sistema
```bash
# Uso de recursos
docker stats --no-stream

# Status dos serviços
make status

# Informações do sistema
make info
```

### Logs Estruturados
```bash
# Logs por serviço
docker-compose logs whisper-insights
docker-compose logs ollama
docker-compose logs nginx  # Modo produção

# Filtrar por nível
docker-compose logs | grep ERROR
docker-compose logs | grep WARNING
```

## 🔄 Atualizações

### Atualizar Aplicação
```bash
# Puxar últimas mudanças
git pull

# Rebuild e restart
docker-compose down
docker-compose up --build -d

# Verificar saúde
make health
```

### Atualizar Modelos
```bash
# Modelos Ollama
docker exec whisper-insights-ollama ollama pull llama3.2
docker exec whisper-insights-ollama ollama list

# Limpar cache Whisper (força redownload)
docker volume rm whispper_insights_whisper_models
```

## 💡 Dicas e Boas Práticas

### Performance
- Use modelo Whisper `tiny` para testes rápidos
- `base` para qualidade equilibrada
- `large` apenas se tiver recursos suficientes

### Segurança
- Mantenha `.env` fora do controle de versão
- Use tokens únicos para produção
- Configure rate limiting adequadamente

### Manutenção
- Execute `docker system prune` regularmente
- Monitore uso de disco dos volumes
- Mantenha backups das configurações

---

**💡 Dica**: Use `make help` para ver todos os comandos disponíveis e `make health` para verificação rápida do status dos serviços.
