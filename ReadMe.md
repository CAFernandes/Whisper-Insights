# 🎙️ Transcritor de Áudio Web com Identificação de Locutores

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

### Opção 3: Com Identificação de Locutores (5 minutos extra)
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

## 🔧 Melhorias Recentes (v2024.05)

### ✅ **Correções Implementadas**
- **Arquivos KWF**: Corrigido erro "Cannot set attribute 'src'" com fallback automático
- **Compatibilidade pyannote.audio 3.3.2**: Atualizado para suportar versão mais recente
- **Warnings suprimidos**: Interface limpa sem mensagens desnecessárias do SpeechBrain
- **Token Hugging Face**: Configuração automática via arquivo .env funcionando 100%
- **🆕 Insights com diarização**: IA agora usa texto estruturado por locutor automaticamente

### 🚀 **Otimizações de Sistema**
- **Detecção inteligente de formato**: Parâmetros otimizados para diferentes tipos de arquivo
- **Fallback robusto**: Sistema se adapta automaticamente quando encontra incompatibilidades
- **Logs informativos**: Mensagens claras para debugging e acompanhamento de status
- **Processamento resiliente**: Aplicação não falha mais com formatos específicos
- **🆕 Hierarquia de texto**: Sistema prioriza diarização > timestamps > texto simples para insights

### 🎯 **Status de Funcionalidades**
- ✅ **Transcrição básica**: 100% funcional para todos os formatos
- ✅ **Timestamps**: Funcionando com fallback automático para KWF
- ✅ **Diarização**: Totalmente operacional com token configurado
- ✅ **Insights IA**: Geração automática via Ollama funcionando
- ✅ **🆕 Insights inteligentes**: Sistema usa automaticamente diarização quando disponível
- ✅ **Interface Web**: Drag & drop e todas as funcionalidades ativas

## 📚 Documentação Completa

### 🎯 **Para Usuários**
- **[⚡ Guia Rápido de Diarização](docs/GUIA_RAPIDO_DIARIZACAO.md)** - Configure identificação de locutores em 5 minutos
- **[📖 Guia Completo de Configuração](docs/DIARIZATION_SETUP.md)** - Instruções detalhadas e solução de problemas

### 🔧 **Para Desenvolvedores**
- **[📋 Documentação Técnica](docs/DIARIZATION_COMPLETE.md)** - Detalhes da implementação de diarização
- **[🚀 Status da Implementação](docs/IMPLEMENTACAO_CONCLUIDA.md)** - Resumo completo do projeto
- **[🔍 Melhoria de Insights](DIARIZATION_INSIGHTS_IMPROVEMENT.md)** - Documentação da melhoria de diarização
- **[✅ Relatório Final](MELHORIA_CONCLUIDA.md)** - Status da implementação da melhoria
- **[🌐 Documentação Web](docs/README-WEB.md)** - Detalhes específicos da interface web

### 📜 **Histórico do Projeto**
- **[📊 Projeto Concluído](docs/PROJETO_CONCLUIDO.md)** - Visão geral das funcionalidades
- **[🔄 Conversão Completa](docs/CONVERSAO_COMPLETA.md)** - Processo de migração desktop → web
- **[✅ Implementações Finalizadas](docs/IMPLEMENTACAO_FINALIZADA.md)** - Log detalhado de mudanças

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

## 📁 Estrutura do Projeto

```
transcribe_audio/
├── 📄 app.py                    # Servidor Flask principal
├── ⚙️ config.py                 # Configurações centralizadas
├── 📁 docs/                     # 📚 Documentação organizada
│   ├── GUIA_RAPIDO_DIARIZACAO.md
│   ├── DIARIZATION_SETUP.md
│   ├── DIARIZATION_COMPLETE.md
│   └── ...
├── 📁 helpers/                  # 🛠️ Utilitários
│   └── file_utils.py
├── 📁 services/                 # 🏗️ Lógica de negócio
│   ├── whisper_service.py       # Transcrição
│   ├── diarization_service.py   # Identificação de locutores
│   ├── ollama_service.py        # Insights IA
│   └── task_service.py          # Gerenciamento de tarefas
├── 📁 templates/                # 🌐 Interface web
│   └── index.html
├── 📁 tests/                    # 🧪 Testes organizados
│   ├── test_units.py            # Testes unitários
│   ├── test_complete_workflow.py # Testes de integração
│   ├── test_dialogue_view.py    # Testes da visualização
│   ├── *.html                   # Páginas de teste
│   ├── demo.sh                  # Script de demonstração
│   └── teste_audio.*            # Arquivos de áudio para teste
├── 📁 uploads/                  # 📂 Arquivos temporários
├── 📋 requirements-web.txt      # Dependências
└── 🚀 start_web.sh             # Script de inicialização
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
1. **📋 Estudar Arquitetura**: Consulte a [documentação técnica completa](docs/DIARIZATION_COMPLETE.md)
2. **🔧 Ver Correções**: Analise as [correções técnicas implementadas](docs/CORRECOES_TECNICAS.md)
3. **🧪 Executar Testes**: `python -m pytest -v` para validar instalação
4. **⚙️ Personalizar**: Modifique `config.py` para suas necessidades específicas

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
- Execute os testes para validar instalação

### **🚀 Tecnologias Utilizadas**
- **Backend**: Flask, OpenAI Whisper, pyannote.audio, Ollama
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **IA**: PyTorch, Transformers, Llama 3.2:3b
- **Testes**: pytest, unittest
- **Deploy**: Gunicorn, Nginx (recomendado)

---

**🎉 Uma aplicação completa de transcrição com IA avançada, pronta para uso profissional!**