# 🎙️ Whisper-Insights

Uma aplicação web profissional para transcrição de áudio usando IA avançada (Whisper + pyannote.audio) com identificação automática de locutores e geração de insights inteligentes.

## ✨ Características Principais

- 🎤 **Identificação de Locutores**: Detecta automaticamente quem está falando em cada momento
- 🌐 **Interface Web Moderna**: Responsiva e intuitiva com drag & drop
- 🔄 **Processamento Assíncrono**: Threading para melhor performance
- 📱 **Design Adaptável**: Funciona perfeitamente em desktop e mobile
- ⚡ **Múltiplos Formatos**: mp3, wav, m4a, ogg, flac, mp4, avi, kwf
- 🧠 **Insights com IA**: Geração automática de resumos e análises (Ollama + Llama)
- **🆕 Insights Inteligentes**: Sistema usa diarização automaticamente para melhor contexto
- 🔒 **Segurança Robusta**: Validação completa de arquivos
- 🧹 **Limpeza Automática**: Gestão inteligente de arquivos temporários
- 🛠️ **Sistema Robusto**: Tratamento inteligente de erros e fallbacks automáticos
- 🧪 **Testes Completos**: Suíte automatizada de testes unitários e integração

## 🚀 Início Rápido

### Pré-requisitos
```bash
# Clone ou baixe o projeto
cd whisper-insights

# Copie o arquivo de configuração
cp .env.example .env

# Edite o arquivo .env com suas configurações
nano .env
```

### Opção 1: Início Simples (Transcrição Básica)
```bash
# 1. Ative o ambiente virtual
source transcribe/bin/activate

# 2. Instale as dependências
pip install -r requirements-web.txt

# 3. Inicie a aplicação
python app.py
```

### Opção 2: Script Automatizado
```bash
./start_web.sh
```

**Acesse**: http://localhost:5001

### Opção 3: Docker (Recomendado para Produção)
```bash
# Clone o projeto
git clone <repository-url>
cd whisper-insights

# Configure o ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Inicie com Docker
docker-compose up -d

# Acesse a aplicação
http://localhost:5001
```

**📖 Guia Completo**: [🐳 Documentação Docker](docs/DOCKER_GUIDE.md)

### Opção 4: Com Identificação de Locutores (5 minutos extra)
Para habilitar a identificação automática de locutores, siga o **[📖 Guia Rápido de Diarização](docs/GUIA_RAPIDO_DIARIZACAO.md)** - leva apenas 5 minutos!

## 🎯 Funcionalidades Disponíveis

### 📝 **Transcrição Básica** (Disponível imediatamente)
- Transcrição simples de áudio para texto
- Transcrição com timestamps palavra por palavra
- Suporte a múltiplos formatos de áudio/vídeo
- **Tratamento otimizado para arquivos KWF** com fallback automático
- **Sistema robusto** que resolve automaticamente conflitos de compatibilidade

### 🎤 **Identificação de Locutores** (Configuração de 5 min)
- Detecta automaticamente quantas pessoas estão falando
- Identifica quem fala em cada momento: `SPEAKER_00`, `SPEAKER_01`, etc.
- Gera resumo estatístico: tempo de fala por pessoa
- Formatos de saída especializados para análise
- **Totalmente funcional** com token do Hugging Face configurado

### 🧠 **Insights Inteligentes** (Opcional)
- Resumo executivo automático
- Identificação de temas principais
- Análise de objetivos e ações
- Classificação do tipo de conteúdo
- **🆕 Uso automático de diarização**: Quando disponível, insights usam texto estruturado por locutor

## 🏗️ Arquitetura Técnica

### Backend (Flask + IA)
- **Flask 3.1.1**: Servidor web robusto
- **OpenAI Whisper**: Transcrição de áudio de alta qualidade
- **pyannote.audio**: Identificação avançada de locutores
- **Ollama + Llama 3.2:3b**: Geração de insights inteligentes
- **Threading**: Processamento assíncrono para melhor performance
- **API RESTful**: Endpoints bem estruturados

### Frontend Moderno
- **HTML5 + CSS3 + JavaScript ES6**: Interface responsiva
- **Drag & Drop**: Upload intuitivo de arquivos
- **Status em Tempo Real**: Feedback visual do processamento
- **Design Adaptável**: Otimizado para desktop e mobile

### IA e Processamento
- **Whisper (PyTorch)**: Transcrição precisa em múltiplos idiomas
- **pyannote.audio**: Diarização (identificação de locutores)
- **Ollama (Docker)**: Análise e geração de insights
- **Sistema de Timeout**: Tratamento robusto de erros

## 📊 Exemplo de Resultados

### 📝 Transcrição Simples
```
Olá, como você está hoje? Eu estou bem, obrigado por perguntar.
```

### ⏰ Com Timestamps
```
[00:00 - 00:03] Olá, como você está hoje?
[00:04 - 00:08] Eu estou bem, obrigado por perguntar.
```

### 🎤 Com Identificação de Locutores
```
[00:00 - 00:03] SPEAKER_00: Olá, como você está hoje?
[00:04 - 00:08] SPEAKER_01: Eu estou bem, obrigado por perguntar.

👥 Resumo dos Locutores:
SPEAKER_00: 15s (60% do tempo)
SPEAKER_01: 10s (40% do tempo)
```

### 🧠 Insights Inteligentes (Ollama)
```
**RESUMO EXECUTIVO**
O áudio contém uma conversa entre duas pessoas sobre estratégias de negócio...

**TEMAS PRINCIPAIS**
1. Planejamento Estratégico
2. Tecnologia e Inovação
3. Comunicação Organizacional

**OBJETIVOS IDENTIFICADOS**
* Definir próximos passos do projeto
* Alinhar expectativas da equipe
* Estabelecer cronograma de entregas

**CLASSIFICAÇÃO**
* Tipo: Reunião de planejamento
* Tom: Profissional e colaborativo
* Duração: 8 minutos
```

## 🏆 Diferenciais da Aplicação

### **🎯 Funcionalidades Avançadas**
- **Identificação de Locutores**: Tecnologia de ponta com pyannote.audio
- **IA Integrada**: Whisper + Llama para transcrição e análise
- **Interface Profissional**: Design moderno e usabilidade excepcional
- **Arquitetura Escalável**: Código modular e bem estruturado

### **🔧 Qualidade Técnica**
- **Testes Completos**: Cobertura abrangente de funcionalidades
- **Tratamento de Erros**: Sistema robusto de fallbacks
- **Performance Otimizada**: Threading e cache inteligente
- **Documentação Completa**: Guias para todos os níveis

### **🚀 Pronto para Produção**
- **Configuração Simples**: Funciona imediatamente
- **Escalabilidade**: Preparado para integração com bancos de dados
- **Segurança**: Validação rigorosa de arquivos
- **Manutenibilidade**: Código limpo e bem documentado

### 🚀 **Começando**
- **[📇 Índice Rápido](docs/INDICE_RAPIDO.md)** - Navegação rápida por toda a documentação
- **[📦 Guia de Instalação](docs/INSTALLATION.md)** - Instalação completa em diferentes sistemas
- **[🐳 Guia Docker](docs/DOCKER_GUIDE.md)** - Deploy com Docker, configuração, monitoramento e troubleshooting
- **[⚙️ Configuração Avançada](docs/CONFIGURATION.md)** - Todas as opções de configuração detalhadas
- **[🔧 Solução de Problemas](docs/TROUBLESHOOTING.md)** - Diagnóstico e resolução de problemas comuns

### 🔌 **Para Desenvolvedores**
- **[🔌 Documentação da API](docs/API_DOCUMENTATION.md)** - API REST completa com exemplos
- **[⚡ Guia Rápido de Diarização](docs/GUIA_RAPIDO_DIARIZACAO.md)** - Configure identificação de locutores em 5 minutos
- **[📖 Configuração de Diarização](docs/DIARIZATION_SETUP.md)** - Instruções detalhadas para diarização
- **[🌐 Documentação Web](docs/README-WEB.md)** - Detalhes específicos da interface web

### 📋 **Referência Técnica**
- **[🔧 Correções Técnicas](docs/CORRECOES_TECNICAS.md)** - Detalhamento das correções implementadas (incluindo Docker health check)
- **[🧪 Guia de Testes](tests/README.md)** - Como executar e criar testes
- **[🔍 Logs e Debugging](docs/TROUBLESHOOTING.md#-ferramentas-de-debug)** - Ferramentas de diagnóstico
- **[🚀 Deploy em Produção](docs/INSTALLATION.md#-deploy-em-produção)** - Configuração para ambiente de produção

## 🧪 Testes e Qualidade

### **Suíte de Testes Automatizados**
- **`tests/test_complete_workflow.py`**: Testa fluxo completo (upload → transcrição → insights)
- **`tests/test_units.py`**: Testes unitários para serviços, utilitários e validações
- **`tests/test_dialogue_view.py`**: Testes da visualização de diálogo
- **`tests/test_diarization_insights.py`**: Testes específicos de diarização
- **Cobertura**: Upload, múltiplos formatos, erros, retry, diarização

### **Executar Testes**
```bash
# Testes unitários
python -m pytest tests/test_units.py -v

# Teste de workflow completo
python tests/test_complete_workflow.py

# Todos os testes
python -m pytest tests/ -v

# Demonstração do sistema
./tests/demo.sh
```

**📋 Guia Completo**: [🧪 Documentação de Testes](tests/README.md)

## 📁 Estrutura do Projeto

```
whisper-insights/
├── 📄 app.py                    # Servidor Flask principal
├── ⚙️ config.py                 # Configurações centralizadas
├── 🔧 .env.example              # Arquivo de configuração exemplo
├── 📋 requirements-web.txt      # Dependências Python
├── 🚀 start_web.sh             # Script de inicialização
├── 📄 cleanup_uploads.py        # Limpeza automática de arquivos
├── 📋 CHANGELOG.md              # Histórico de versões
├── 📁 docs/                     # 📚 Documentação organizada
│   ├── INSTALLATION.md          # Guia de instalação detalhado
│   ├── CONFIGURATION.md         # Configurações avançadas
│   ├── API_DOCUMENTATION.md     # Documentação da API
│   ├── TROUBLESHOOTING.md       # Solução de problemas
│   ├── GUIA_RAPIDO_DIARIZACAO.md # Guia rápido de diarização
│   ├── DIARIZATION_SETUP.md     # Setup detalhado de diarização
│   └── README-WEB.md            # Documentação da interface web
├── 📁 helpers/                  # 🛠️ Utilitários
│   ├── __init__.py
│   └── file_utils.py           # Utilitários de arquivo
├── 📁 services/                 # 🏗️ Lógica de negócio
│   ├── __init__.py
│   ├── whisper_service.py       # Transcrição com Whisper
│   ├── diarization_service.py   # Identificação de locutores
│   ├── ollama_service.py        # Insights com IA
│   └── task_service.py          # Gerenciamento de tarefas
├── 📁 public/                   # 🌐 Arquivos estáticos
│   └── assets/
│       ├── css/main.css         # Estilos da aplicação
│       └── js/main.js           # JavaScript da interface
├── 📁 templates/                # 🌐 Templates HTML
│   └── index.html              # Interface principal
├── 📁 tests/                    # 🧪 Testes automatizados
│   ├── __init__.py
│   ├── README.md               # Guia de testes
│   ├── test_units.py            # Testes unitários
│   ├── test_complete_workflow.py # Testes de integração
│   ├── test_dialogue_view.py    # Testes da visualização
│   ├── demo.sh                  # Script de demonstração
│   └── teste_audio.*            # Arquivos de áudio para teste
├── 📁 legacy/                   # 📜 Arquivos antigos
│   ├── README.md               # Documentação de arquivos legacy
│   └── transcritor_audio.py    # Versão desktop original
├── 📁 uploads/                  # 📂 Arquivos temporários (auto-criado)
└── 📁 transcribe/               # 🐍 Ambiente virtual Python
```

## 🏆 Diferenciais da Aplicação

### **🎯 Funcionalidades Avançadas**
- **Identificação de Locutores**: Tecnologia de ponta com pyannote.audio
- **IA Integrada**: Whisper + Llama para transcrição e análise
- **Interface Profissional**: Design moderno e usabilidade excepcional
- **Arquitetura Escalável**: Código modular e bem estruturado

### **🔧 Qualidade Técnica**
- **Testes Completos**: Cobertura abrangente de funcionalidades
- **Tratamento de Erros**: Sistema robusto de fallbacks
- **Performance Otimizada**: Threading e cache inteligente
- **Documentação Completa**: Guias para todos os níveis

### **🚀 Pronto para Produção**
- **Configuração Simples**: Funciona imediatamente
- **Escalabilidade**: Preparado para integração com bancos de dados
- **Segurança**: Validação rigorosa de arquivos
- **Manutenibilidade**: Código limpo e bem documentado

## 💡 Deployment e Produção

### **🚀 Para Produção**
```bash
# Usando Gunicorn (recomendado)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Com Nginx como proxy reverso
# Configure nginx.conf para fazer proxy para localhost:8000
```

### **🔧 Melhorias para Ambiente Empresarial**
- **Banco de Dados**: Integre PostgreSQL/MySQL para histórico de transcrições
- **Autenticação**: Adicione login/logout para multiusuários
- **Monitoramento**: Configure logs estruturados e métricas
- **Cache**: Redis para cache de resultados e sessões
- **API Keys**: Sistema de tokens para controle de acesso

### **📊 Monitoramento**
- Logs detalhados em `app.log`
- Métricas de performance integradas
- Sistema de limpeza automática de uploads
- Tratamento robusto de timeouts e erros

## 🎯 Próximos Passos

### **👤 Para Usuários**
1. **🚀 Começar Agora**: Execute `python app.py` e acesse http://localhost:5001
2. **🎤 Habilitar Diarização**: Siga o [📖 Guia Rápido](docs/GUIA_RAPIDO_DIARIZACAO.md) (5 minutos)
3. **📁 Testar Formatos**: Sistema suporta todos os formatos, incluindo KWF com fallback automático
4. **🔍 Explorar Recursos**: Teste diferentes opções de visualização e exports

### **👨‍💻 Para Desenvolvedores**
1. **📋 Estudar Arquitetura**: Consulte a [📦 documentação de instalação](docs/INSTALLATION.md)
2. **⚙️ Configuração**: Analise as [⚙️ configurações avançadas](docs/CONFIGURATION.md)
3. **🧪 Executar Testes**: `python -m pytest -v` para validar instalação
4. **🔌 Integrar API**: Use a [🔌 documentação da API](docs/API_DOCUMENTATION.md)

### **🏢 Para Empresas**
1. **🌐 Deploy**: Configure Gunicorn + Nginx para produção
2. **🔗 Integração**: Conecte com sistemas existentes via API RESTful robusta
3. **📈 Escalar**: Adicione banco de dados e autenticação conforme necessário
4. **📊 Monitorar**: Use logs detalhados e métricas integradas

---

## 📞 Suporte e Contribuição

### **📖 Documentação**
- Toda documentação está organizada na pasta **[📁 docs/](docs/)**
- Guias específicos para cada funcionalidade
- Instruções passo-a-passo para configuração

### **🐛 Problemas ou Dúvidas**
- Consulte primeiro os guias na pasta `docs/`
- Verifique os logs em `app.log`
- Execute os testes para validar instalação: `python -m pytest tests/ -v`
- Consulte o [🔧 Guia de Solução de Problemas](docs/TROUBLESHOOTING.md)

### **🚀 Tecnologias Utilizadas**
- **Backend**: Flask, OpenAI Whisper, pyannote.audio, Ollama
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **IA**: PyTorch, Transformers, Llama 3.2:3b
- **Testes**: pytest, unittest
- **Deploy**: Gunicorn, Nginx (recomendado)

---

**🎉 Uma aplicação completa de transcrição com IA avançada, pronta para uso profissional!**

## 📈 Status Atual (Junho 2025)
- ✅ **100% Operacional** - Todos os recursos funcionando
- 🐳 **Docker Pronto** - Deploy em containers totalmente suportado
- 🔧 **Correções Aplicadas** - Health check e outras melhorias implementadas
- 📚 **Documentação Completa** - Guias para todos os cenários
- 🧪 **Testes Validados** - Suíte completa de testes automatizados

📇 **[Índice Rápido](docs/INDICE_RAPIDO.md)** | 📋 **[Changelog](CHANGELOG.md)** | 🔧 **[Configuração](.env.example)** | 📚 **[Documentação](docs/)** | 🧪 **[Testes](tests/)**