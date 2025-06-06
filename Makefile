# ====================================
# Whisper-Insights - Makefile
# ====================================
# Comandos para gerenciar o projeto Docker

.PHONY: help build up down logs restart clean prune health test

# Configurações
DOCKER_COMPOSE = docker-compose
IMAGE_NAME = whisper-insights
CONTAINER_NAME = whisper-insights-app

# ====================================
# Comandos Principais
# ====================================

help: ## 📋 Mostra esta ajuda
	@echo "🎙️ Whisper-Insights - Comandos Docker"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## 🔨 Constrói as imagens Docker
	@echo "🔨 Construindo imagens Docker..."
	$(DOCKER_COMPOSE) build --no-cache

up: ## 🚀 Inicia todos os serviços
	@echo "🚀 Iniciando serviços..."
	$(DOCKER_COMPOSE) up -d
	@echo "✅ Serviços iniciados!"
	@echo "🌐 Aplicação: http://localhost:5001"
	@echo "🤖 Ollama: http://localhost:11434"

up-dev: ## 🔧 Inicia em modo desenvolvimento (com logs)
	@echo "🔧 Iniciando em modo desenvolvimento..."
	$(DOCKER_COMPOSE) up

down: ## 🛑 Para todos os serviços
	@echo "🛑 Parando serviços..."
	$(DOCKER_COMPOSE) down

restart: ## 🔄 Reinicia todos os serviços
	@echo "🔄 Reiniciando serviços..."
	$(DOCKER_COMPOSE) restart

# ====================================
# Logs e Monitoramento
# ====================================

logs: ## 📋 Mostra logs de todos os serviços
	$(DOCKER_COMPOSE) logs -f

logs-app: ## 📋 Mostra logs apenas da aplicação
	$(DOCKER_COMPOSE) logs -f whisper-insights

logs-ollama: ## 📋 Mostra logs apenas do Ollama
	$(DOCKER_COMPOSE) logs -f ollama

health: ## 🏥 Verifica saúde dos serviços
	@echo "🏥 Verificando saúde dos serviços..."
	@echo "📱 Aplicação Principal:"
	@curl -s http://localhost:5001/health | python3 -m json.tool || echo "❌ Aplicação não responde"
	@echo "\n🤖 Ollama:"
	@curl -s http://localhost:11434/api/tags | python3 -m json.tool || echo "❌ Ollama não responde"

# ====================================
# Gerenciamento de Dados
# ====================================

volumes: ## 📁 Lista volumes Docker
	@echo "📁 Volumes Docker:"
	@docker volume ls | grep whisper

backup-volumes: ## 💾 Backup dos volumes
	@echo "💾 Fazendo backup dos volumes..."
	@mkdir -p backups/$(shell date +%Y%m%d_%H%M%S)
	@docker run --rm -v whisper-insights_whisper_models:/data -v $(PWD)/backups/$(shell date +%Y%m%d_%H%M%S):/backup alpine tar czf /backup/whisper_models.tar.gz -C /data .
	@docker run --rm -v whisper-insights_ollama_data:/data -v $(PWD)/backups/$(shell date +%Y%m%d_%H%M%S):/backup alpine tar czf /backup/ollama_data.tar.gz -C /data .
	@echo "✅ Backup concluído em backups/$(shell date +%Y%m%d_%H%M%S)/"

# ====================================
# Limpeza e Manutenção
# ====================================

clean: ## 🧹 Remove containers parados
	@echo "🧹 Removendo containers parados..."
	docker container prune -f

clean-images: ## 🧹 Remove imagens não utilizadas
	@echo "🧹 Removendo imagens não utilizadas..."
	docker image prune -f

clean-volumes: ## ⚠️ Remove volumes não utilizados (CUIDADO!)
	@echo "⚠️ ATENÇÃO: Isso removerá volumes não utilizados!"
	@read -p "Tem certeza? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	docker volume prune -f

prune: ## 🧹 Limpeza completa (containers, images, networks)
	@echo "🧹 Limpeza completa do Docker..."
	docker system prune -f

reset: ## 🔄 Reset completo (para e remove tudo)
	@echo "🔄 Reset completo..."
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f
	@echo "✅ Reset concluído!"

# ====================================
# Desenvolvimento e Debug
# ====================================

shell: ## 🐚 Acessa shell do container principal
	@echo "🐚 Acessando shell do container..."
	docker exec -it $(CONTAINER_NAME) /bin/bash

shell-ollama: ## 🐚 Acessa shell do container Ollama
	@echo "🐚 Acessando shell do Ollama..."
	docker exec -it whisper-insights-ollama /bin/bash

test: ## 🧪 Executa testes dentro do container
	@echo "🧪 Executando testes..."
	docker exec -it $(CONTAINER_NAME) python -m pytest tests/ -v

test-api: ## 🧪 Testa API via curl
	@echo "🧪 Testando API..."
	@echo "📱 Health Check:"
	@curl -s http://localhost:5001/health
	@echo "\n🤖 Ollama Status:"
	@curl -s http://localhost:11434/api/tags

# ====================================
# Produção
# ====================================

prod-up: ## 🏭 Inicia em modo produção (com Nginx)
	@echo "🏭 Iniciando em modo produção..."
	$(DOCKER_COMPOSE) --profile production up -d
	@echo "✅ Produção iniciada!"
	@echo "🌐 Aplicação: http://localhost"

prod-down: ## 🏭 Para modo produção
	@echo "🏭 Parando modo produção..."
	$(DOCKER_COMPOSE) --profile production down

# ====================================
# Modelos e Setup
# ====================================

download-models: ## 📥 Baixa modelos essenciais do Ollama
	@echo "📥 Baixando modelos do Ollama..."
	docker exec -it whisper-insights-ollama ollama pull llama3.2
	docker exec -it whisper-insights-ollama ollama pull mistral
	@echo "✅ Modelos baixados!"

list-models: ## 📋 Lista modelos do Ollama
	@echo "📋 Modelos do Ollama:"
	docker exec -it whisper-insights-ollama ollama list

# ====================================
# Informações
# ====================================

status: ## 📊 Status completo dos serviços
	@echo "📊 Status dos Serviços:"
	@echo "======================"
	$(DOCKER_COMPOSE) ps
	@echo "\n🔍 Uso de recursos:"
	@docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

info: ## ℹ️ Informações do sistema
	@echo "ℹ️ Informações do Sistema:"
	@echo "========================="
	@echo "🐳 Docker: $(shell docker --version)"
	@echo "🏗️ Docker Compose: $(shell docker-compose --version)"
	@echo "💾 Espaço em disco:"
	@df -h | head -2
	@echo "🔍 Volumes Docker:"
	@docker volume ls | grep whisper || echo "Nenhum volume encontrado"

# ====================================
# Configuração inicial
# ====================================

init: ## 🎬 Configuração inicial completa
	@echo "🎬 Configuração inicial do Whisper-Insights..."
	@echo "1️⃣ Verificando arquivos..."
	@[ -f .env ] || (echo "⚠️ Criando .env..." && cp .env.example .env)
	@echo "2️⃣ Construindo imagens..."
	@$(MAKE) build
	@echo "3️⃣ Iniciando serviços..."
	@$(MAKE) up
	@echo "4️⃣ Aguardando inicialização..."
	@sleep 30
	@echo "5️⃣ Verificando saúde..."
	@$(MAKE) health
	@echo "✅ Configuração inicial concluída!"
	@echo "🌐 Acesse: http://localhost:5001"

# ====================================
# Por padrão, mostra a ajuda
# ====================================
.DEFAULT_GOAL := help